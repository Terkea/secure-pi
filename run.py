import json

from securepi import app

if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
    app.run(host=data['NETWORK']['IPv4_address'], port=data['NETWORK']['running_port'], debug=True)
