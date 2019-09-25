from flask import Flask, escape, request, render_template, redirect, url_for, session
from securepi import app, tools
from securepi.forms import LoginForm
from securepi.models import User, Email, Picture, WhiteList

TEMPERATURE = tools.measure_temp()
MEMORY_AVAILABLE = tools.get_machine_storage()

@app.route('/')
def index():
    return render_template('index.html', temperature_value = TEMPERATURE, memory_available_value = MEMORY_AVAILABLE)

@app.route('/logout')
def logout():
    del session['email']
    return redirect(url_for('index'))


# if there's no email in the session is gonna force the user to login
@app.before_request
def require_login():
    allowed_routes = ['login']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = str(form.email.data)
        password = (str(form.password.data))
        print("email:  {}, password: {}".format(email, password))

        # rootAccount = User(email='test@root.com', password=tools.encrypt('secure-pi'))
        # db.session.add(rootAccount)
        # db.session.commit()

        # CHECK DB FOR ACCOUNT
        query = User.query.filter_by(email=email).first()
        if query:
            print('email found')
            if tools.check_hash(form.password.data, query.password):
                print('password match with email')
                session['email'] = form.email.data
                return redirect(url_for('index'))
            else:
                print('doesn\'t match')
                form.email.errors.append('Invalid account')
        else:
            print('couldn\'t find email address')
            form.email.errors.append('Invalid account')

    else:
        print("FAIL")
    return render_template('login.html', form=form)

@app.route('/smtp/', methods=['GET', 'POST'])
def smtp():
    return render_template('smtp.html')