from flask import Flask, escape, request, render_template
from securepi import app, tools

TEMPERATURE = tools.measure_temp()
MEMORY_AVAILABLE = tools.get_machine_storage()

@app.route('/')
def index():
    return render_template('index.html', temperature_value = TEMPERATURE, memory_available_value = MEMORY_AVAILABLE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')