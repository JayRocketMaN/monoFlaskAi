from flask import Flask, render_template, request, redirect, flash, jsonify, session, url_for
import os, re, requests
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm, ResetPasswordForm
from dotenv import load_dotenv
from launchGenai import generate 
from extension import db
from authlib.integrations.flask_client import OAuth
from models import Users
from itsdangerous import URLSafeTimedSerializer
from configure import brevo_reset_email
from flask_bcrypt import Bcrypt


monoFlask = Flask(__name__)

load_dotenv()
monoFlask.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
monoFlask.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
monoFlask.config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')
monoFlask.config['BREVO_API_KEY'] = os.getenv('BREVO_API_KEY')
monoFlask.config["MONGO_URI"] = os.getenv('MONGO_URI')
monoFlask.config["FLASK_DEBUG"] = os.getenv('FLASK_DEBUG')
monoFlask.config['MONGODB_SETTINGS'] = {'host': os.getenv('MONGO_URI')}
bcrypt = Bcrypt(monoFlask)
db.init_app(monoFlask)
# Initialize OAuth
oauth = OAuth(monoFlask)
# Required for testing OAuth locally over HTTP (Remove this in production!)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
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
login_manager.init_app(monoFlask)
login_manager.login_view = 'submit'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"
# load user
@login_manager.user_loader
def load_user(user_id):
    return Users.objects(id=user_id).first()

@monoFlask.route('/')
@login_required
def chat():
    return render_template('chat.html')

@monoFlask.route('/signup')
def signup():
    form = RegistrationForm()
    return render_template('signup.html', form=form)

@monoFlask.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@monoFlask.route('/forgotPassword')
def forgotPassword():
    return render_template('forgotPassword.html')

@monoFlask.route('/resetPassword')
def resetPassword():
    form = ResetPasswordForm()
    return render_template('resetPassword.html', form=form)


@monoFlask.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    #session.clear()
    return render_template('logout.html')



@monoFlask.route('/getIn/<source>')
def getIn(source):
    client = getattr(oauth, source, None)
    if client:
        redirect_uri = url_for('auth', source=source, _external=True)
        return client.authorize_redirect(redirect_uri)
    return "Provider not supported", 404

@monoFlask.route('/auth/<source>')
def auth(source):
    #fetch user info from the provider
    client = getattr(oauth, source, None)
    if not client:
        return "Invalid provider", 404
    # get token from Google/Facebook
    token = client.authorize_access_token()
    
    if source == 'google':
        user_data = token.get('userinfo')
    else:
        #for Facebook a manual profile fetch
        resp = client.get('me?fields=id,name,email')
        user_data = resp.json()

    if user_data:
        #check if the email is verified
        if not user_data.get('email_verified', True):
            return "Email not verified by provider", 400
        
        #check for user in MongoDB
        user = Users.objects(email=user_data['email']).first()
        
        if not user:
            # create new user if user don't exist
            user = Users(
                fullname=user_data.get('name'),
                email=user_data['email'],
                username=user_data['email'].split('@')[0]
            )
            #password placeholder
            user.password_hash = "oauth_user" 
            user.save()
        
        #session logic
        login_user(user)        
        return redirect(url_for('chat'))

    return "Authentication failed", 401

                

@monoFlask.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            fullname = form.fullname.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            confirmPassword = form.confirmPassword.data
            #save user to mongoDB
            new_user= Users(fullname=fullname, email=email, username=username)
            new_user.set_password(password) 
            new_user.save()
            flash(f'Account created for {username}, Login to Chat!', 'success')
            return redirect('/signup')
        except Exception as e:
             flash(f'Account creation failed, Try again!', 'error')
             print(f'--error: {str(e)}')
    
    return render_template('signup.html', form=form)

@monoFlask.route("/submit" , methods=['POST'])
def submit():
    form = LoginForm()
    try:
        email = form.email.data
        password = form.password.data
        user = Users.objects(email = email).first()
        if user and user.check_password(password):
             login_user(user)
             return redirect('/')
        else:
            flash(f'Either the Email or Password is invalid, Try again!', 'error')
    except Exception as e:
            print(f'--python error: {str(e)}')

    return render_template('login.html', form=form)
 
    
@monoFlask.route('/response', methods=['POST'])
@login_required
def AiResponse():
    userInput = request.json.get('message')
    final_response = generate(userInput)
    return jsonify({'response': final_response})

@monoFlask.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    
    if request.method == 'POST':
        email = request.form.get('email')

        user = Users.objects(email=email).first()
        if user:
            #Generate token
            serializer = URLSafeTimedSerializer(monoFlask.config['SECRET_KEY'])
            token = serializer.dumps(email, salt='password-reset-salt')
       
            #Create absolute URL for the reset link
            reset_url = url_for('reset_token', token=token, _external=True)
                            
            #Send via Brevo
            if brevo_reset_email(email, reset_url):
                flash('If an account exists with that email, a reset link has been sent.', 'success')
                                
            else:
                flash('There was an issue sending the email. Please try again later.', 'error')
                return redirect(url_for('forgotPassword')) # Redirect back to resetPasswordHtml
        else:
            flash('the email does not exist', 'error')    
    return render_template('forgotPassword.html') 

@monoFlask.route('/reset_token/<token>', methods=['GET','POST'])
def reset_token(token):
    form = ResetPasswordForm()
    serializer = URLSafeTimedSerializer(monoFlask.config['SECRET_KEY'])
    if form.validate_on_submit():
        try:
            #Verify token to expire in 15 minutes (900 seconds)
            email = serializer.loads(token, salt='password-reset-salt', max_age=900)
            password = form.password.data
        except:
            flash('The password reset link is invalid or has expired.', 'error')
            return redirect(url_for('reset_request'))
        
        #check for user
        user = Users.objects(email=email).first()
        if user:
            user.set_password(password)
            user.save()
            flash('Your password has been updated! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'error')
        
        return redirect(url_for('login'))        
    return render_template('resetPassword.html', form=form, token=token)#ResetPasswordForm
        
if __name__ == '__main__':
    monoFlask.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
    
    