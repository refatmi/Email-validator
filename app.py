from flask import Flask, request, jsonify
import smtplib
import dns.resolver
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

def check_email_smtp(email):
    domain = email.split('@')[-1]
    
    # Get MX records
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mail_server = str(mx_records[0].exchange)
    except:
        return {"email": email, "valid": False, "reason": "Invalid domain or no MX records"}

    # Connect to the mail server
    try:
        server = smtplib.SMTP(mail_server, timeout=10)
        server.helo()
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return {"email": email, "valid": True, "reason": "Valid email"}
        else:
            return {"email": email, "valid": False, "reason": "Invalid recipient"}
    except:
        return {"email": email, "valid": False, "reason": "SMTP connection failed"}

@app.route('/validate-email', methods=['GET'])
def validate_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    result = check_email_smtp(email)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
