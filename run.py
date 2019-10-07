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
from securepi.camera import VideoCamera
from flask import Response


PROFILE_FACE = cv2.CascadeClassifier('haarcascades/haarcascade_profileface.xml')
FRONTAL_FACE = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
UPPER_BODY = cv2.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')
FULL_BODY = cv2.CascadeClassifier('haarcascades/haarcascade_fullbody.xml')

OBJECT_CLASSIFIERS = [PROFILE_FACE, FRONTAL_FACE, UPPER_BODY, FULL_BODY]

UPDATE_INTERVAL = 50 # only once in this time interval
VIDEO_CAMERA = VideoCamera(flip=False) # creates a camera object, flip vertically
COUNTER = 0

def check_for_objects():
    global COUNTER
    while True:
        try:
            for object_classifier in OBJECT_CLASSIFIERS:
                frame, found_obj = VIDEO_CAMERA.check_for_object(object_classifier)
                if found_obj and (time.time() - COUNTER) > UPDATE_INTERVAL:
                    COUNTER = time.time()
                    now = datetime.now()
                    print("{} OBJECT DETECTED".format(now.strftime("%d/%m/%Y_%H:%M:%S")))
                    VIDEO_CAMERA.get_image()
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
    app.run(host='0.0.0.0', debug=False)

