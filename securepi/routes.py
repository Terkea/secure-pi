#!/usr/bin/env python3

from flask import Flask, escape, request, render_template, redirect, url_for, session, Response, jsonify, make_response
from securepi import app, tools, db
from securepi.forms import LoginForm, UpdateSMTPForm, UpdateEmailAddress, AddNewEmail, SettingsForm
from securepi.models import User, Email, Records
import json
import cv2

# CONSTANTS
TEMPERATURE = tools.measure_temp()
MEMORY_AVAILABLE = tools.get_machine_storage()
with open('config.json') as json_file:
    CONFIG = json.load(json_file)


@app.route('/')
def index():
    return render_template('index.html', temperature_value=TEMPERATURE, memory_available_value=MEMORY_AVAILABLE)


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

    # todo check if the email is unique
    if "form3-submit" in request.form and form3.validate_on_submit():
        email = str(form3.email.data)
        newemail = Email(email=email, notifications=True)

        db.session.add(newemail)
        db.session.commit()
        query = Email.query.all()

    return render_template('smtp.html', config=CONFIG['SMTP'], query=query, form=form, form2=form2, form3=form3,
                           temperature_value=TEMPERATURE, memory_available_value=MEMORY_AVAILABLE)


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


@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()

    if form.validate_on_submit():
        CONFIG['SETTINGS']['picture_resolution'] = str(form.picture_resolution.data)
        CONFIG['SETTINGS']['brightness'] = str(form.brightness.data)
        CONFIG['SETTINGS']['contrast'] = str(form.contrast.data)
        CONFIG['SETTINGS']['saturation'] = str(form.saturation.data)
        CONFIG['SETTINGS']['how_often_to_take_pictures'] = str(form.how_often_to_take_pictures.data)
        CONFIG['SETTINGS']['border_color'] = str(form.border_color.data)
        CONFIG['SETTINGS']['store_location'] = str(form.store_location.data)

        print('FILE UPDATED')

        with open('config.json', 'w') as f:
            f.write(json.dumps(CONFIG))
            f.close()

    else:
        print('FAIL')

    return render_template('settings.html', config=CONFIG, temperature_value=TEMPERATURE,
                           memory_available_value=MEMORY_AVAILABLE, form=form)


@app.route('/live_view/', methods=['GET', 'POST'])
def live_view():
    return render_template('live_view.html', temperature_value=TEMPERATURE,
                    memory_available_value=MEMORY_AVAILABLE)

@app.route("/records", methods=['GET', 'POST'])
def records():
    return render_template('records.html')

@app.route("/load", methods=['GET', 'POST'])
def load():
    if request.args.get("start_date") != "null" or request.args.get("last_date") != "null":
        database = [i.serialize for i in
                    db.session.query(Records).filter(Records.created_at >= request.args.get("start_date"),
                                                     Records.created_at <= request.args.get("last_date")).all()]
        print("search args found")
    else:
        database = [i.serialize for i in Records.query.order_by(Records.id.desc()).all()]
        print("all records, no search args")

    posts = len(database)  # num posts to generate
    quantity = 21  # num posts to return per request

    # time.sleep(0.2)  # Used to simulate delay

    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(database[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify(database[counter: counter + quantity]), 200)

    return res

@app.route("/records/search", methods=['GET', 'POST'])
def search_records():
    # sql = "SELECT * FROM records"
    # result = db.engine.execute(sql)
    # names = [Records for row in result]
    # print(type(names[0]))

    database = [i.serialize for i in db.session.query(Records).filter(Records.created_at >= "1/10/2019",
                                                                      Records.created_at <= "15/10/2019").all()]
    return make_response(jsonify(database))