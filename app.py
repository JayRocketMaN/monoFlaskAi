from flask import Flask, render_template, request, redirect, flash, jsonify, session
import os, re
from dotenv import load_dotenv
from launchGenai import generate 

monoFlask = Flask(__name__)

load_dotenv()
monoFlask.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@monoFlask.route('/')
def chat():
    return render_template('chat.html')

@monoFlask.route('/signup')
def signup():
    return render_template('signup.html')

@monoFlask.route('/login')
def login():
    return render_template('login.html')

@monoFlask.route('/forgotPassword')
def forgotPassword():
    return render_template('forgotPassword.html')


@monoFlask.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

EMAIL_REGEX = r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'
@monoFlask.route('/register', methods=['POST'])
def register():
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get( 'confirmPassword')
        if len(fullname) < 3:
            flash('fullname is too short', 'error')
            return redirect('/signup')
        if not re.fullmatch(EMAIL_REGEX, email, re.IGNORECASE):
            flash('invalid email')
            return redirect('/signup')
        if len(username) > 10:
            flash('username is too long', 'error')
            return redirect('/signup')
        # if password != 'Bucon21)':
        #     flash('incorrect password')
        #     return redirect('/signup')
        if confirmPassword != password:
            flash('passwords does not match')
            return redirect('/signup')
        else:
            return redirect('/')
        
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
    
    