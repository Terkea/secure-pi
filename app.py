from flask import Flask, escape, request, render_template
import cv2
import numpy
import tools
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///securepi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}')"




TEMPERATURE = tools.measure_temp()
MEMORY_AVAILABLE = tools.get_machine_storage()

@app.route('/')
def index():
    return render_template('index.html', temperature_value = TEMPERATURE, memory_available_value = MEMORY_AVAILABLE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
