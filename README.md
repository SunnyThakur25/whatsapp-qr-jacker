![ad909e54-e63d-4b9a-b423-d992de0acca8](https://github.com/user-attachments/assets/e7948feb-d6e0-499a-8999-5cbf72aa7de4)




# WhatsApp QRLJacking Tool

A cutting-edge red team tool engineered for simulating WhatsApp session hijacking via QR code phishing (QRLJacking). Built with a modern Streamlit GUI, a Flask-based phishing server, Selenium for QR code extraction, and Nginx/Certbot for production-grade HTTPS deployment, this tool replicates WhatsApp's login page to entice targets into scanning a QR code, capturing session data for authorized security assessments. Last updated: June 20, 2025.
Disclaimer: This tool is intended exclusively for ethical hacking and authorized red team engagements. Unauthorized use or distribution is illegal and unethical. Obtain explicit consent and adhere to all applicable laws. This repository is private—do not make it public.
Features

Advanced GUI: Cyberpunk-themed Streamlit interface with custom branding, real-time logging, and intuitive controls.
Realistic Phishing: HTTPS-enabled phishing page mimicking WhatsApp's official login with dynamic lures.
Social Engineering: Configurable lures (group invites, channel promos, urgent logins) with obfuscated URLs.
Secure Deployment: Nginx reverse proxy with Certbot SSL for production-grade security and stealth.
Modular Architecture: Clean separation of QR extraction, phishing server, and lure generation components.

Prerequisites
```
Operating System: Ubuntu 20.04+ (or equivalent Linux distribution).
Dependencies:
Python 3.8+
Tesseract OCR
Chromedriver (compatible with installed Chrome version)
Nginx
Certbot
```

Infrastructure:
Registered domain with DNS pointing to the server’s public IP.
Root or sudo privileges for deployment.


Assets:

Custom whatsappqr_logo.png in static/ (recommended: 150x150px PNG).

Installation

Clone the repository:
```
git clone https://github.com/yourusername/whatsapp_qrljacker.git
cd whatsapp_qrljacker
```

Install system dependencies:
```
sudo apt update
sudo apt install -y python3 python3-venv nginx certbot python3-certbot-nginx tesseract-ocr
```

Install Python dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
Install Chromedriver:
```
Download from https://chromedriver.chromium.org/downloads.
Match your Chrome version and add to PATH.
```

Add logo:
```
Place whatsappqr_logo.png in the static/ directory.
```


Configuration

Edit config/config.yaml:
```
Set phishing_url to your domain (e.g., https://yourdomain.com).
Adjust lure_type (options: group_invite, channel_promo, urgent_login).
```

Modify config/nginx.conf:
```
Replace yourdomain.com with your domain.
```

Update scripts/deploy.sh:
```
Replace yourdomain.com and your.email@example.com with your details.
```


Deployment

Make the deployment script executable:```chmod +x scripts/deploy.sh```


Execute the deployment:```./scripts/deploy.sh```


Configures the virtual environment, starts the Flask server, sets up Nginx, and secures with Certbot SSL.



Usage

Access the GUI:
```
Open http://localhost:8501 in your browser.
View the whatsappqr_logo.png in the sidebar for branding.
Select a lure type and generate a message for distribution (email, SMS, social media).
```

Start Phishing Server:
```
Click "Start Phishing Server" to extract the QR code and host at https://yourdomain.com.
QR code displays in the GUI.
```

Monitor Logs:
```
Check real-time logs in the GUI or logs/qrl_jacker.log for session captures.
```

Stop Server:
```
Click "Stop Phishing Server" to terminate the Flask server.
```


Red Team Tactics
```
Phishing Realism: HTTPS page mimics WhatsApp’s login with lures like "Join our exclusive group!".
Lure Deployment: Distribute messages with short URLs (e.g., https://wa.me/abc123) via targeted campaigns.
Stealth Operations: Nginx security headers and HTTPS evade basic detection.
Session Exploitation: Logs capture session data upon QR scan.
```
Security Notes
```
Authorization: Deploy only with explicit target organization approval.
Stealth: Use an anonymous domain and private repository to avoid traceability.
Maintenance: Renew SSL certificates with sudo certbot renew.
Customization: Tailor templates/phishing.html for campaign-specific pretexts.
Logo: Ensure whatsappqr_logo.png is unique and untraceable.
```
Project Structure
```
src/: Core scripts (GUI, QR extraction, phishing server, lures).
templates/: Phishing page HTML.
config/: Configuration (YAML, Nginx).
logs/: Session and error logs.
static/: QR code and whatsappqr_logo.png.
scripts/: Deployment script.
requirements.txt: Dependencies.
run.sh: Local development script.
```
Troubleshooting
```
QR Extraction Failure: Verify Chromedriver and Tesseract installation.
Server Issues: Validate Nginx config (sudo nginx -t) and port availability.
Logo Display: Confirm whatsappqr_logo.png is in static/.
Logs: Review logs/qrl_jacker.log for errors.
```
Contributing
```
Fork the repository.
Create a feature branch (git checkout -b feature/new-lure).
Commit changes (git commit -m "Add new lure type").
Push and submit a pull request.
```
License
For authorized use only. No warranty provided. Use at your own risk.
Repository

URL: https://github.com/SunnyThakur25/whatsapp_qrljacker.git
Access: Restricted to authorized team members.

Contact
For issues or enhancements, contact your red team lead or open an issue in this repository.
