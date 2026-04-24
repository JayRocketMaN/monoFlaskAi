import os
import requests
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
 

load_dotenv()
oauth = OAuth()


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


# Register Google OAuth
google = oauth.register(
        name='google',
        client_id= os.getenv('CLIENT_ID'),
        client_secret= os.getenv('CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
# Register Facebook OAuth
facebook = oauth.register(
        name='facebook',
        client_id= os.getenv('FB_CLIENT_ID'),
        client_secret= os.getenv('FB_CLIENT_SECRET'),
        access_token_url='https://graph.facebook.com/v19.0/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/v19.0/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/v19.0/',
        client_kwargs={'scope': 'email public_profile'},
    )
class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    APP_NAME = os.getenv('APP_NAME', 'AI ChatBox')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    BREVO_API_KEY = os.getenv('BREVO_API_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT', 8000))  
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGO_URI'),
        'connect': False 
    }


class DevelopmentConfig(Config):
    DEBUG=True
  

class ProductionConfig(Config):
    DEBUG=False
     
    
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)

