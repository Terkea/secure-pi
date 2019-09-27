import json
from datetime import datetime
from threading import Timer

from securepi import app, tools

x = datetime.today()
y = x.replace(day=x.day + 1, hour=1, minute=0, second=0, microsecond=0)
delta_t = y - x

secs = delta_t.seconds + 1

if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
    app.run(host=data['NETWORK']['IPv4_address'], port=data['NETWORK']['running_port'], debug=True)

    t = Timer(secs, tools.update_config())
    t.start()
