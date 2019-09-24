from flask import Flask, escape, request, render_template
import cv2
import numpy
import os
import time
import tools

app = Flask(__name__)

TEMPERATURE = tools.measure_temp()
MEMORY_AVAILABLE = tools.get_machine_storage()

@app.route('/')
def index():
    return render_template('index.html', temperature_value = TEMPERATURE, memory_available_value = MEMORY_AVAILABLE)

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
