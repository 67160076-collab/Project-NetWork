# Papaya Web Engineering & Security Architecture Project

โปรเจกต์ระบบเว็บแอปพลิเคชัน WordPress บนสถาปัตยกรรม LEMP Stack บน Microsoft Azure VM พร้อมการปรับแต่งความปลอดภัย (Security Hardening) และระบบ AI Log Scanner

## 🛠️ Tech Stack & Infrastructure

- **Infrastructure:** Microsoft Azure Ubuntu Linux VM
- **Domain & SSL:** DuckDNS (`papayapogpog.duckdns.org`), Let's Encrypt (Certbot HTTPS)
- **Web Server:** Nginx (Reverse Proxy & Web Server)
- **Database:** MySQL
- **Runtime:** PHP 8.3-FPM
- **CMS:** WordPress (Theme: Kadence)
- **Security:** Fail2ban, UFW Firewall, SSH Key PKI, PHP Hardening, Nginx Access Control Rules
- **Monitoring & Analytics:** AI Log Scanner (Python), Security Dashboard

---

## 📁 Repository Structure

```text
.
├── .gitignore               # บล็อกไฟล์ความลับและความจุสูง
├── .env.example             # ตัวอย่างแม่แบบ Environment Variables
├── README.md                # เอกสารอธิบายโปรเจกต์
├── content/                 # ไฟล์ส่งออกเนื้อหาเว็บไซต์ (.xml)
│   └── computerscience.WordPress.xml
├── theme/                   # ไฟล์คอนฟิกและธีมเว็บไซต์
│   └── kadence-theme-export.dat
├── nginx/                   # คอนฟิกูเรชัน Nginx Web Server
│   └── papaya.conf
├── scripts/                 # สคริปต์วิเคราะห์และตรวจจับภัยคุกคาม
│   └── ai_log_scanner.py
└── dashboard/               # หน้าแสดงผล Security Dashboard
    └── index.html
```
