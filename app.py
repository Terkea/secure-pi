from flask import Flask, escape, request
import cv2
import numpy
import os
import time
import tools as tools
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    print(tools.measure_temp())
    print(tools.get_machine_storage())
    return f'Hello, {escape(name)}!'

if __name__ == '__main__':
    app.run()
