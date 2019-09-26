from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Field required')])

class UpdateSMTPForm(FlaskForm):
    server = StringField('Server', validators=[DataRequired(message='Field required')])
    email = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Field required')])
    port = StringField('Port', validators=[DataRequired(message='Field required')])

class UpdateEmailAddress(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])