import json

from securepi import app

if __name__ == '__main__':
    with open('config.json') as json_file:
        data = json.load(json_file)
    app.run(host=data['NETWORK']['local_ip'], port=data['NETWORK']['running_port'], debug=True)
