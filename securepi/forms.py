#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Field required')])


class UpdateSMTPForm(FlaskForm):
    server = StringField('Server', validators=[DataRequired(message='Field required')])
    email = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Field required')])
    port = StringField('Port', validators=[DataRequired(message='Field required')])


class UpdateAccount(FlaskForm):
    email_update = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])
    old_password = PasswordField('Old password', validators=[DataRequired(message='field required')])
    password = PasswordField('Password', validators=[DataRequired(message='field required')])
    confirm_password = PasswordField('Password', validators=[DataRequired(message='field required')])
    id = StringField('ID', validators=[DataRequired(message='Field required')])


class CreateNewAccount(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='field required')])
    confirm_password = PasswordField('Password', validators=[DataRequired(message='field required')])
