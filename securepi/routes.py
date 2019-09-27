from flask import Flask, escape, request, render_template, redirect, url_for, session
from securepi import app, tools, db
from securepi.forms import LoginForm, UpdateSMTPForm, UpdateEmailAddress, AddNewEmail
from securepi.models import User, Email, Picture, WhiteList
import json


#CONSTANTS
TEMPERATURE = tools.measure_temp()
MEMORY_AVAILABLE = tools.get_machine_storage()
with open('config.json') as json_file:
    CONFIG = json.load(json_file)



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
    form = UpdateSMTPForm(request.form)
    form2 = UpdateEmailAddress(request.form)
    form3 = AddNewEmail(request.form)
    query = Email.query.all()

    if "form-submit" in request.form and form.validate_on_submit():
        email = str(form.email.data)
        password = str(form.password.data)
        server = str(form.server.data)
        port = str(form.port.data)

        if tools.test_email(server, port, email, password):
            CONFIG['SMTP']['server'] = server
            CONFIG['SMTP']['port'] = port
            CONFIG['SMTP']['username'] = email
            CONFIG['SMTP']['password'] = password

            with open('config.json', 'w') as f:
                f.write(json.dumps(CONFIG))
                f.close()
        else:
            form.server.errors.append(
                "Invalid account, be sure that you have less secure app access turned on or try with a gmail account")

    if "form2-submit" in request.form and form2.validate_on_submit():
        query = Email.query.get(str(form2.id.data))
        query.email = str(form2.email_update.data)
        db.session.commit()
        query = Email.query.all()

    #todo check if the email is unique
    if "form3-submit" in request.form and form3.validate_on_submit():
        email = str(form3.email.data)
        newemail = Email(email=email, notifications=True)

        db.session.add(newemail)
        db.session.commit()
        query = Email.query.all()

    return render_template('smtp.html', config=CONFIG['SMTP'], query=query, form=form, form2=form2, form3=form3, temperature_value = TEMPERATURE, memory_available_value = MEMORY_AVAILABLE)

@app.route('/delete_email/<int:id>', methods=['GET', 'POST'])
def delete_email(id):
    query = Email.query.get_or_404(id)

    try:
        db.session.delete(query)
        db.session.commit()
        return redirect(url_for('smtp'))
    except:
        return 'There was a problem deleting that email'


@app.route('/change_notification_status/<int:id>', methods=['GET', 'POST'])
def change_notification_status(id):
    query = Email.query.get_or_404(id)

    try:
        if query.notifications == True:
            query.notifications = False
            db.session.commit()
            return redirect(url_for('smtp'))
        else:
            query.notifications = True
            db.session.commit()
            return redirect(url_for('smtp'))
    except:
        return 'There was a problem changing the notification status on that email'


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    print(tools.get_hostname())
    # todo gotta check the configuration before rendering the view
    return render_template('settings.html', config=CONFIG, temperature_value = TEMPERATURE, memory_available_value = MEMORY_AVAILABLE)