from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyzbar.pyzbar as pyzbar
from PIL import Image
import time
import base64
import logging
import os

def init_driver() -> webdriver.Chrome:
    """Initialize headless Chrome WebDriver."""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        logging.info("WebDriver initialized")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize WebDriver: {str(e)}")
        raise

def extract_qr_code(target_url: str, qr_image_path: str) -> str | None:
    """Extract QR code from target URL and save as image."""
    try:
        driver = init_driver()
        driver.get(target_url)
        time.sleep(5)  # Wait for QR code to load
        screenshot_path = "screenshot.png"
        driver.get_screenshot_as_file(screenshot_path)
        img = Image.open(screenshot_path)
        qr_codes = pyzbar.decode(img)
        driver.quit()
        os.remove(screenshot_path)  # Clean up
        if qr_codes:
            qr_data = qr_codes[0].data.decode()
            os.makedirs(os.path.dirname(qr_image_path), exist_ok=True)
            with open(qr_image_path, "wb") as f:
                f.write(base64.b64decode(qr_data.split(",")[1]) if "," in qr_data else qr_data)
            logging.info(f"QR code extracted and saved to {qr_image_path}")
            return qr_data
        else:
            logging.error("No QR code found in screenshot")
            return None
    except Exception as e:
        logging.error(f"Error extracting QR code: {str(e)}")
        return None