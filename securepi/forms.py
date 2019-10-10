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


class UpdateEmailAddress(FlaskForm):
    email_update = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])
    id = StringField('ID', validators=[DataRequired(message='Field required')])


class AddNewEmail(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='Field required'), Email()])


class SettingsForm(FlaskForm):
    picture_resolution = StringField('Picture resolution',
                                     validators=[DataRequired(message='Picture resolution Field required')])
    brightness = StringField('Brightness', validators=[DataRequired(message='Brightness Field required')])
    contrast = StringField('Contrast', validators=[DataRequired(message='Contrast Field required')])
    saturation = StringField('Saturation', validators=[DataRequired(message='Saturation Field required')])
    how_often_to_take_pictures = StringField('How often', validators=[DataRequired(message='How often Field required')])
    border_color = StringField('Border color', validators=[DataRequired(message='Border color Field required')])
    store_location = StringField('Store location', validators=[DataRequired(message='Store location Field required')])
