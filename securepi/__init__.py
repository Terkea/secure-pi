#!/usr/bin/env python3

from flask import Flask
from flask_jsglue import JSGlue
from flask_sqlalchemy import SQLAlchemy
from securepi import forms

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'SEX BOT'
jsglue = JSGlue()
jsglue.init_app(app)
db = SQLAlchemy(app)

from securepi import routes
from securepi import DetectorAPI