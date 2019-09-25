# import json
#
# config = {}
#
# #this represents the smtp server which will send the notification emails
# config['SMTP'] = {
#         'server': 'smtp.gmail.com',
#         'username': 'test@gmail.com',
#         'password': 'password',
#         'port': '465',
#         'ssl': 'true',
# }
#
# config['NETWORK'] = {
#         'local_ip' : '192.168.1.65',
#         'public_ip' : '86.185.8.125',
#         'running_port' : '5000'
# }
#
# config['SETTINGS'] = {
#         'picture_resolution' : '1920x1080',
#         'brightness' : '0-100 value',
#         'contrast' : '0-100 value',
#         'saturation' : '0-100 value',
#         'how_often_to_take_pictures' : '5s',
#         'DHCP_notifications' : 'boolean',
#         'logs' : 'boolean',
#         'text_overlay' : 'app_name + datetime'
# }
#
# with open('config.json', 'w') as f:
#     f.write(json.dumps(config))
#     f.close()