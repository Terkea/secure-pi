from flask import Flask, escape, request, render_template, redirect, url_for, flash
from securepi import app, tools
from securepi.forms import LoginForm

TEMPERATURE = tools.measure_temp()
MEMORY_AVAILABLE = tools.get_machine_storage()

@app.route('/')
def index():
    return render_template('index.html', temperature_value = TEMPERATURE, memory_available_value = MEMORY_AVAILABLE)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = str(form.email.data)
        password = tools.encrypt(str(form.password.data))
        print("email:  {}, password: {}".format(email, password))
        print('SUCCESS')
        return redirect(url_for('index'))
    else:
        flash('Input a valid account')
        print("FAIL")
    return render_template('login.html', form=form)