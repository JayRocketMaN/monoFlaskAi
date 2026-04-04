from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import re

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


class RegistrationForm(FlaskForm):
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