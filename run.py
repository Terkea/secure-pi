#!/usr/bin/env python3

import json
import cv2
import sys
import time
import threading
import numpy as np
from datetime import datetime
from threading import Timer
from picamera import PiCamera
from securepi import app, tools
from securepi.DetectorAPI import DetectorAPI
from securepi.camera import VideoCamera
from flask import Response
from securepi.models import User, Email, Records
from securepi import db
import imageio



UPDATE_INTERVAL = 5 # only once in this time interval
VIDEO_CAMERA = VideoCamera(flip=False) # creates a camera object, flip vertically
API = DetectorAPI()
THRESHOLD = 0.7

def check_for_objects():
    while True:
        try:
            time.sleep(UPDATE_INTERVAL)
            tools.update_config()
            frame_in_bytes = VIDEO_CAMERA.get_frame()
            #Convert the frame from bytes to nparray so it can be processed by the API
            decoded = cv2.imdecode(np.frombuffer(frame_in_bytes, np.uint8), -1)
            boxes, scores, classes, num = API.processFrame(decoded)

            for i in range(len(boxes)):
                # Class 1 represents human
                if classes[i] == 1 and scores[i] > THRESHOLD:
                    box = boxes[i]
                    cv2.rectangle(decoded,(box[1],box[0]),(box[3],box[2]),(0,0,255),2)
                    color_conversion = cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB)
                    now = datetime.now()
                    imageio.imwrite('securepi/static/records/{}.jpg'.format(now.strftime("%d-%m-%Y_%H:%M:%S")), color_conversion)

                    #update database
                    new_record = Records(created_at = now.strftime("%d/%m/%Y %H:%M:%S"), file_type = "picture", path_filename = "{}.jpg".format(now.strftime("%d-%m-%Y_%H:%M:%S")))
                    db.session.add(new_record)
                    db.session.commit()
        except:
            print("Error: ", sys.exc_info()[0])

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VIDEO_CAMERA),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()

    #TODO CHECK EVERY ONCE AN HOUR IF THE IP ADDRESS IS THE SAME OR SEND MAIL WITH NEW ONE

    app.run(host='0.0.0.0', debug=False)

