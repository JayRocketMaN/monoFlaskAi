import os
import requests
#from werkzeug.security import generate_password_hash
#from itsdangerous import URLSafeTimedSerializer
# User model and db setup:
# from models import db, User 


def brevo_reset_email(email, reset_url):
    api_key = os.getenv("BREVO_API_KEY") 
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"name": "monoFlask AI Chat", "email": "odidikaanthony02@gmail.com"},
        "to":[{"email": email}],
        "subject": "Password Reset",
        "htmlContent": f"""
            <h3>Hello,</h3>
            <p>You requested a password reset. Click the link below to reset it:</p>
            <p><a href="{reset_url}">Reset My Password</a></p>
            <p>If you did not request this, please ignore this email.</p>
            <p>This link will expire in 15 minutes.</p>
        """
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code in [201, 200]

