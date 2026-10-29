import json, os, subprocess, urllib.request, urllib.error, datetime

cfg = {}
for line in open(os.path.expanduser("~/.logtools.env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()

team = {x.strip() for x in cfg.get("TEAM_IPS", "").split(",") if x.strip()}
raw = subprocess.run(["python3", os.path.expanduser("~/logtools/parse_logs.py")], capture_output=True, text=True).stdout
summary = json.loads(raw)

def mask(v):
    if isinstance(v, list):
        out = []
        for item in v:
            if isinstance(item, list) and item and item[0] in team:
                continue
            out.append(mask(item))
        return out
    if isinstance(v, dict):
        return {k: mask(x) for k, x in v.items()}
    return v

safe = mask(summary)

prompt = ("คุณเป็นนักวิเคราะห์ความปลอดภัยของเซิร์ฟเวอร์ ด้านล่างคือสถิติ log 24 ชั่วโมงล่าสุดของ VPS ที่รันเว็บ WordPress (SSH และ Nginx) ช่วยวิเคราะห์เป็นภาษาไทย ตอบเป็น JSON เท่านั้น ไม่ใส่ markdown รูปแบบ: "
    '{"risk_level":"low|medium|high","summary":"สรุป 2-3 ประโยค","threats":[{"title":"","detail":"","ips":[""]}],"recommendations":["",""]}'
    "\n\nมาตรการที่ทีมทำแล้ว (ห้ามแนะนำซ้ำ): ปิดล็อกอิน SSH ด้วยรหัสผ่าน, ปิด root login, ใช้ SSH key เท่านั้น, ติดตั้ง fail2ban, เปิด HTTPS แล้ว. สิ่งที่ยังไม่ได้ทำ (แนะนำได้): firewall geo-block, บล็อกไฟล์ขึ้นต้นด้วยจุดใน Nginx, reverse proxy/Cloudflare, rate limit หน้า wp-login"
    "\n\nข้อมูล:\n" + json.dumps(safe, ensure_ascii=False))
model = cfg.get("GEMINI_MODEL", "gemini-3.8-flash")
url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent"
body = {"contents": [{"parts": [{"text": prompt}]}]}
result = {"generated_at": datetime.datetime.now().isoformat(timespec="seconds"), "stats": summary}
import time
base_url = "https://generativelanguage.googleapis.com/v1beta/models/"
def call(m):
    rq = urllib.request.Request(base_url + m + ":generateContent", data=json.dumps(body).encode(), headers={"x-goog-api-key": cfg["GEMINI_API_KEY"], "content-type": "application/json"})
    with urllib.request.urlopen(rq, timeout=120) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"].strip()
text = None
err = ""
for n, m in enumerate([model, model, "gemini-3.5-flash-lite", "gemini-3.5-flash-lite"]):
    try:
        text = call(m)
        break
    except urllib.error.HTTPError as e:
        err = "HTTP " + str(e.code) + ": " + e.read().decode()[:200]
        if e.code not in (429, 500, 503):
            break
    except Exception as e:
        err = str(e)
    time.sleep(20 * (n + 1))
if text is not None:
    t = text
    if t.startswith("```"):
        t = t.strip("`")
        if t.lower().startswith("json"):
            t = t[4:]
    try:
        result["ai"] = json.loads(t)
    except Exception:
        result["ai"] = {"raw": text}
else:
    result["ai"] = {"error": err}
    try:
        old = json.load(open(os.path.expanduser("~/logtools/output/ai_report.json")))["ai"]
        if "risk_level" in old:
            old["stale"] = True
            result["ai"] = old
    except Exception:
        pass

os.makedirs(os.path.expanduser("~/logtools/output"), exist_ok=True)
path = os.path.expanduser("~/logtools/output/ai_report.json")
with open(path, "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(json.dumps(result["ai"], ensure_ascii=False, indent=2))
print("saved:", path)