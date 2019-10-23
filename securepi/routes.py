#!/usr/bin/env python3
from datetime import datetime, timedelta

from flask import Flask, escape, request, render_template, redirect, url_for, session, Response, jsonify, make_response
from securepi import app, tools, db
from securepi.forms import LoginForm, UpdateSMTPForm, UpdateAccount, CreateNewAccount
from securepi.models import User, Records
import json
import cv2

with open('config.json') as json_file:
    CONFIG = json.load(json_file)


@app.route('/')
def index():
    today_date = datetime.today().strftime("%Y-%m-%d")
    week = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    month = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

    all_records = len(Records.query.order_by(Records.id).all())

    today_records = len(db.session.query(Records).filter(Records.created_at.between(today_date, today_date)).all())

    last_7_days = len(db.session.query(Records).filter(Records.created_at.between(week, today_date)).all())

    last_30_days = len(db.session.query(Records).filter(Records.created_at.between(month, today_date)).all())

    data = [all_records,
            today_records,
            last_7_days,
            last_30_days]

    chart_data = []

    for i in range(1, 31):
        chart_data.append(len(db.session.query(Records).filter(Records.created_at.between(
            (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d"),
            (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d"))).all()))

    TEMPERATURE = tools.measure_temp()
    MEMORY_AVAILABLE = tools.get_machine_storage()

    return render_template('index.html', temperature_value=TEMPERATURE, memory_available_value=MEMORY_AVAILABLE,
                           data=data, config=CONFIG, chart_data=chart_data)


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

@app.route('/live_view/', methods=['GET', 'POST'])
def live_view():
    TEMPERATURE = tools.measure_temp()
    MEMORY_AVAILABLE = tools.get_machine_storage()

    return render_template('live_view.html', temperature_value=TEMPERATURE,
                    memory_available_value=MEMORY_AVAILABLE)

@app.route("/records", methods=['GET', 'POST'])
def records():
    TEMPERATURE = tools.measure_temp()
    MEMORY_AVAILABLE = tools.get_machine_storage()
    return render_template('records.html', temperature_value=TEMPERATURE,
                           memory_available_value=MEMORY_AVAILABLE)

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

@app.route("/settings/accounts/", methods=['GET', 'POST'])
def accounts():
    TEMPERATURE = tools.measure_temp()
    MEMORY_AVAILABLE = tools.get_machine_storage()
    form2 = UpdateAccount()
    form3 = CreateNewAccount()
    query = User.query.all()


    if "form2-submit" in request.form and form2.validate_on_submit():
        query = User.query.get(str(form2.id.data))
        if tools.check_hash(str(form2.old_password.data), query.password):
            password = str(form2.password.data)
            confirm_password = str(form2.confirm_password.data)
            if (password == confirm_password):
                query.email = str(form2.email_update.data)
                query.password = tools.encrypt(password)
                db.session.commit()
        query = User.query.all()

    # todo check if the email is unique
    if "form3-submit" in request.form and form3.validate_on_submit():
        email = str(form3.email.data)
        password = str(form3.password.data)
        confirm_password = str(form3.confirm_password.data)
        if(password == confirm_password):
            user = User(email=email,password=tools.encrypt(password), notifications=True)
            db.session.add(user)
            db.session.commit()

        query = User.query.all()

    return render_template('accounts.html', config=CONFIG['SMTP'], query=query, form2=form2, form3=form3,
                           temperature_value=TEMPERATURE, memory_available_value=MEMORY_AVAILABLE)

@app.route('/settings/smtp/', methods=['GET', 'POST'])
def smtp():
    TEMPERATURE = tools.measure_temp()
    MEMORY_AVAILABLE = tools.get_machine_storage()


    form = UpdateSMTPForm(request.form)
    form2 = UpdateAccount(request.form)
    form3 = CreateNewAccount(request.form)
    query = User.query.all()

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

    return render_template('smtp.html', config=CONFIG['SMTP'], query=query, form=form, form2=form2, form3=form3,
                           temperature_value=TEMPERATURE, memory_available_value=MEMORY_AVAILABLE)