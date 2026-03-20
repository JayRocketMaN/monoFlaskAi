from flask import Flask, render_template, request, redirect, flash, jsonify, session, url_for
import os, re, requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from dotenv import load_dotenv
from launchGenai import generate 
from authlib.integrations.flask_client import OAuth
from mongodb import mongoConnect
from itsdangerous import URLSafeTimedSerializer
from configure import brevo_reset_email
from werkzeug.security import generate_password_hash


monoFlask = Flask(__name__)

load_dotenv()
monoFlask.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
monoFlask.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
monoFlask.config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')
monoFlask.config['BREVO_API_KEY'] = os.getenv('BREVO_API_KEY')
# Initialize OAuth
oauth = OAuth(monoFlask)

# Required for testing OAuth locally over HTTP (Remove this in production!)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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

@monoFlask.route('/')
def chat():
    return render_template('chat.html')

@monoFlask.route('/signup')
def signup():
    form = RegisterationForm()
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
def logout():
    session.pop('user', None)
    #session.clear()
    return render_template('logout.html')


@monoFlask.route('/getIn/<source>')
def getIn(source):
    if source == 'google':
        redirect_uri = url_for('auth', source='google', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)
    elif source  == 'facebook':
        redirect_uri = url_for('auth', source='facebook', _external=True)
        return oauth.facebook.authorize_redirect(redirect_uri)
    return "Provider not supported", 404

@monoFlask.route('/auth/<source>')
def auth(source):
    if source == 'google':
        token = oauth.google.authorize_access_token()
        # Google returns user info inside the token if openid is used
        user = token.get('userinfo')
        
    elif source == 'facebook':
        token = oauth.facebook.authorize_access_token()
        # Fetch user details using the access token
        resp = oauth.facebook.get('me?fields=id,name,email,picture')
        user = resp.json()

    if user:
        # Save user info in the session
        session['user'] = user
        
    return redirect(url_for('chat'))   
                
def passwordCustom(form, field):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
    password = field.data
    if not any(char.isdigit() for char in password):
          raise ValidationError('Password must contain at least a digit')
    if not any(char.isalpha() for char in password):
        raise ValidationError('Password must contain at least an alphabet')
    if len(password) < 8:
         raise ValidationError('Password must be more than 8 character')
    if(regex.search(password) == None):
         raise ValidationError('Password must contain a special character')
class RegisterationForm(FlaskForm):
        fullname = StringField('fullname', validators=[DataRequired()])
        email = EmailField('Email', validators=[DataRequired(), Email()])
        username = StringField('username', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired(), passwordCustom])
        confirmPassword = PasswordField('confirmpassword', validators=[DataRequired(), EqualTo('password', message='password does not match')])
        submit = SubmitField('CREATE ACCOUNT')
class LoginForm(FlaskForm):
     email = EmailField('Email', validators=[DataRequired(), Email()])
     password = PasswordField('password', validators=[DataRequired(), passwordCustom]) 
     submit = SubmitField('LOGIN') 

class ResetPasswordForm(FlaskForm):
        password = PasswordField('password', validators=[DataRequired(), passwordCustom])
        confirmPassword = PasswordField('confirmpassword', validators=[DataRequired(), EqualTo('password', message='password does not match')])
        submit = SubmitField('UPDATE PASSWORD')

@monoFlask.route('/register', methods=['POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        try:
            fullname = form.fullname.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            confirmPassword = form.confirmPassword.data
            flash(f'Account created for {username}, Login to Chat!', 'success')
            return redirect('/signup')
        except Exception as e:
             print(f'--error: {str(e)}')
    
    return render_template('signup.html', form=form)

@monoFlask.route("/submit" , methods=['POST'])
def submit():
    form = LoginForm()
    if form.validate_on_submit():
            try:
                email = form.email.data
                password = form.password.data
                return redirect('/')
            except Exception as e:
                print(f'--python error: {str(e)}')

    return render_template('login.html', form=form)

# def submit(value, field, form):
#     value = ['bucon', 'true']
#     form = LoginForm()

#     if field.Password in value:
#         raise ValidationError('password is not correct')
#     print (ValidationError)
#     flash ('incorrect password')
#     return redirect('/')
# def submit():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect('/')
#     return render_template('login.html', form=form)
    
    
@monoFlask.route('/response', methods=['POST'])
def AiResponse():
    userInput = request.json.get('message')
    final_response = generate(userInput)
    return jsonify({'response': final_response})

@monoFlask.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    
    if request.method == 'POST':
        email = request.form.get('email')

        #Generate token
        serializer = URLSafeTimedSerializer(monoFlask.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='password-reset-salt')
        
        #Create absolute URL for the reset link
        reset_url = url_for('reset_token', token=token, _external=True)
            
           # 4. Send via Brevo
        if brevo_reset_email(email, reset_url):
                 flash('If an account exists with that email, a reset link has been sent.', 'success')
                     
        else:
             flash('There was an issue sending the email. Please try again later.', 'error')
        return redirect(url_for('forgotPassword')) # Redirect back to resetPassword
        
    return render_template('forgotPassword.html') 

@monoFlask.route('/reset_token/<token>', methods=['GET','POST'])
def reset_token(token):
    form = ResetPasswordForm()
    serializer = URLSafeTimedSerializer(monoFlask.config['SECRET_KEY'])
    try:
        # Verify token. max_age=900 means it expires in 15 minutes (900 seconds)
        email = serializer.loads(token, salt='password-reset-salt', max_age=900)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('reset_request'))
    
    if form.validate_on_submit():
        
       # Update user in DB
       # hashed_password = generate_password_hash(new_password)
        # user = User.query.filter_by(email=email).first()
        # user.password = hashed_password
        # db.session.commit()
        
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))
        
    # the "Enter New Password" form
    return render_template('resetPassword.html', form=form, token=token) 
        
# print('testing mongodb')
# mongoConnect()

if __name__ == '__main__':
    monoFlask.run(debug= True, host="0.0.0.0",port=8090)
    
    