from flask import Flask, jsonify, request
import ssl

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "system": "Secure Banking Gateway (Legacy)",
        "message": "Welcome to the secure portal. Please login."
    })

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/transfer', methods=['POST'])
def transfer():
    return jsonify({"status": "processing", "id": "TXN_123456"}), 200

if __name__ == '__main__':
    # Use the WEAK certificate generated in Dockerfile
    context = ('/etc/pki/tls/certs/vulnerable.crt', '/etc/pki/tls/private/vulnerable.key')
    app.run(host='0.0.0.0', port=443, ssl_context=context, debug=False)
