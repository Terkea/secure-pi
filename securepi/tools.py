import os
import ssl
import sys
import urllib
from urllib import request
import bcrypt
import smtplib
import json
import socket


from securepi.models import Email

with open('config.json') as json_file:
    CONFIG = json.load(json_file)

# Check if os is linux
def linux_interaction():
    if (sys.platform.startswith('linux')):
        return True
    else:
        return False

# returns CPU temp
def measure_temp():
    try:
        if linux_interaction() == True:
            temp = os.popen("vcgencmd measure_temp").readline()
            return (temp.replace("temp=", "")).strip()
        else:
            return ('n\\a')
    except:
        return ('n\\a')

# returns Storage available
def get_machine_storage():
    try:
        if linux_interaction() == True:
            result = os.statvfs('/')
            block_size = result.f_frsize
            total_blocks = result.f_blocks
            free_blocks = result.f_bfree
            # giga=1024*1024*1024
            giga = 1000 * 1000 * 1000
            total_size = total_blocks * block_size / giga
            free_size = free_blocks * block_size / giga
            return ('%s GB' % free_size)
        else:
            return ('n\\a')
    except:
        return ('n\\a')


#PASSWORD ENCRYPTION
def encrypt(string):
    salt = bcrypt.gensalt(rounds=8)
    hash = bcrypt.hashpw(string.encode('utf-8'), salt)
    return hash

#PASSWORD CHECK IF HASH CORESPONDS TO STRING
def check_hash(string, hash):
    if bcrypt.checkpw(string.encode('utf-8'), hash.encode('utf-8')):
        return True
    else:
        return False


#check if credentials are working
def test_email(server, port, username, password):
    try:
        server = smtplib.SMTP_SSL(server, port)
        server.ehlo()
        server.login(username, password)
        return True
    except:
        return False
    finally:
        server.quit()

# TODO NOT TESTED YET, ALSO NEED TO CHECK IF IT WORKS WITH A LIST OF REVIECERS
def send_email(message, subject):
    try:
        # CREATE THE EMAIL
        message = 'Subject: Secure-pi | {}\n\n{}'.format(subject, message)

        query = Email.query.filter_by(notifications=True).all()
        context = ssl.create_default_context()

        server = smtplib.SMTP_SSL(CONFIG['SMTP']['server'], CONFIG['SMTP']['port'])
        server.ehlo()
        server.login(CONFIG['SMTP']['username'], CONFIG['SMTP']['password'])

        for email in query:
            server.sendmail(CONFIG['SMTP']['username'], email.email, message)
            print(email)
            print('mail send succesfully')
    except:
        print('Couldn\'t send email')
        return False
    finally:
        server.quit()
        
def get_public_ip():
    ip = urllib.request.urlopen('http://checkip.amazonaws.com/')
    return ip.read().decode("utf-8")

def get_ipv4():
    hostname = socket.gethostname()
    IPv4_Addr = socket.gethostbyname(hostname)
    return IPv4_Addr

def get_hostname():
    hostname = socket.gethostname()
    return hostname

def update_config():
    if CONFIG['NETWORK']['public_ip'] != get_public_ip():
        send_email("""It looks like your IPS just changed your IP address \n
        Don't worry, we got you :D \n
        The new IP address is {}:{}""".format(get_public_ip()), CONFIG['NETWORK']["running_port"], "DHCP Notification")
        CONFIG['NETWORK']['public_ip'] = get_public_ip()
        with open('config.json', 'w') as f:
            f.write(json.dumps(CONFIG))
            f.close()

    if CONFIG['NETWORK']['IPv4_address'] != get_ipv4():
        CONFIG['NETWORK']['IPv4_address'] = get_ipv4()
        with open('config.json', 'w') as f:
            f.write(json.dumps(CONFIG))
            f.close()

    if CONFIG['NETWORK']['hostname'] != get_hostname():
        CONFIG['NETWORK']['hostname'] = get_hostname()
        with open('config.json', 'w') as f:
            f.write(json.dumps(CONFIG))
            f.close()