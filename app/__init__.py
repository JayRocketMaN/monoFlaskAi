from flask import Flask, render_template, redirect, url_for, session
from flask_login import current_user
import os
from flask_login import LoginManager, login_required, logout_user
from app.forms.allForms import RegistrationForm, LoginForm, ResetPasswordForm
from dotenv import load_dotenv
from app.extension import oauth
from flask_bcrypt import Bcrypt
from app.extension import db
from app.config import get_config

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    load_dotenv()

    # Initialize extensions
    bcrypt = Bcrypt(app)
    db.init_app(app)
    oauth.init_app(app)
  
   
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
        client_id= os.getenv('CLIENT_ID'),
        client_secret= os.getenv('CLIENT_SECRET'),
        access_token_url='https://graph.facebook.com/v19.0/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/v19.0/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/v19.0/',
        client_kwargs={'scope': 'email public_profile'},
    )
    
    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.submit'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "danger"

    from app.models.allModels import Users    
    from app.routes.auth.authRoutes import auth_bp
    from app.routes.user.userAuth import user_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
        
    # load user
    @login_manager.user_loader
    def load_user(user_id):
        return Users.objects(id=user_id).first()

   
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('user.chat'))
        return redirect(url_for('auth.submit')) 

    @app.route('/signup')
    def signup():
        form = RegistrationForm()
        return render_template('signup.html', form=form)

    @app.route('/login')
    def login():
        form = LoginForm()
        return render_template('login.html', form=form)

    @app.route('/forgotPassword')
    def forgotPassword():
        return render_template('forgotPassword.html')

    @app.route('/resetPassword')
    def resetPassword():
        form = ResetPasswordForm()
        return render_template('resetPassword.html', form=form)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.pop('user', None)
        #session.clear()
        return render_template('logout.html')
                     
    return app

app = create_app()

        
        