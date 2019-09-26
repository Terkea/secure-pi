from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from securepi import forms

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'SEX BOT'
db = SQLAlchemy(app)

from securepi import routes