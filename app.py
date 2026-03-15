from flask import Flask, render_template, request, redirect, flash, jsonify, session, url_for
import os, re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from dotenv import load_dotenv
from launchGenai import generate 
from authlib.integrations.flask_client import OAuth

monoFlask = Flask(__name__)

load_dotenv()
monoFlask.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
monoFlask.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
monoFlask.config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')

# Initialize OAuth
oauth = OAuth(monoFlask)

# Required for testing OAuth locally over HTTP (Remove this in production!)
#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'



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
    return render_template('login.html')

@monoFlask.route('/forgotPassword')
def forgotPassword():
    return render_template('forgotPassword.html')


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
       if type(field.data) != str: 
          flash('password cannot be numbers')
class RegisterationForm(FlaskForm):
        fullname = StringField('fullname', validators=[DataRequired()])
        email = EmailField('Email', validators=[DataRequired(), Email()])
        username = StringField('username', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired(), passwordCustom])
        confirmPassword = PasswordField('confirmpassword', validators=[DataRequired(), EqualTo('password', message='password does not match')])
        submit = SubmitField('register')



# class LoginForm(FlaskForm):
#      email = EmailField('email', validators=[DataRequired(), Email()])
#      password = PasswordField('password', validators=[DataRequired() ])  

EMAIL_REGEX = r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'
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
            flash(f'Account created for {username}, Login to Chat!')
            return redirect('/signup')
        except Exception as e:
             print(f'--error: {str(e)}')
    
    return redirect('/signup')
# def register():
#         fullname = request.form.get('fullname')
#         email = request.form.get('email')
#         username = request.form.get('username')
#         password = request.form.get('password')
#         confirmPassword = request.form.get( 'confirmPassword')
#         if len(fullname) < 3:
#             flash('fullname is too short', 'error')
#             return redirect('/signup')
#         if not re.fullmatch(EMAIL_REGEX, email, re.IGNORECASE):
#             flash('invalid email')
#             return redirect('/signup')
#         if len(username) > 10:
#             flash('username is too long', 'error')
#             return redirect('/signup')
#         # if password != 'Bucon21)':
#         #     flash('incorrect password')
#         #     return redirect('/signup')
#         if confirmPassword != password:
#             flash('passwords does not match')
#             return redirect('/signup')
#         else:
#             return redirect('/')
        
@monoFlask.route("/submit" , methods=['POST'])

def submit():
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None and not re.fullmatch(EMAIL_REGEX, email, re.IGNORECASE):
                flash('invalid email')
                return redirect('/login')
        if password != 'Bucon21)':
            flash('incorrect password')
            return redirect('/login')
        
        return redirect('/')

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

@monoFlask.route('/reset_password', methods=['POST'])
def reset():
     email = request.form.get('email')
     
     if email is None and not re.fullmatch(EMAIL_REGEX, email, re.IGNORECASE):
          flash('invalid email')
          return redirect('/forgotPassword')
     else:
          return render_template('chat.html')
     

if __name__ == '__main__':
    monoFlask.run(debug= True)
    
    