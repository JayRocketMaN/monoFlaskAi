from flask import Flask, render_template, request, redirect, flash, jsonify, session, url_for
import os, re, requests
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from app.forms.allForms import RegistrationForm, LoginForm, ResetPasswordForm
from dotenv import load_dotenv
from app.launchGenai import generate 
from app.extension import oauth
from app.models.allModels import Users
from itsdangerous import URLSafeTimedSerializer
from app.config import brevo_reset_email
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone
from flask import Blueprint, request, current_app
from app.extension import db



auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['POST'])
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


@auth_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    form = LoginForm()
    if request.method == 'POST':
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


@auth_bp.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    
    if request.method == 'POST':
        email = request.form.get('email')

        user = Users.objects(email=email).first()
        if user:
            #Generate token
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
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

@auth_bp.route('/reset_token/<token>', methods=['GET','POST'])
def reset_token(token):
    form = ResetPasswordForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
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

@auth_bp.route('/getIn/<source>')
def getIn(source):
        client = getattr(oauth, source, None)
        if client:
            redirect_uri = url_for('auth.email_auth', source=source, _external=True)
            return client.authorize_redirect(redirect_uri)
        return "Provider not supported", 404

@auth_bp.route('/auth/<source>')
def email_auth(source):
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