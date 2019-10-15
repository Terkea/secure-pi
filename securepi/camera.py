#!/usr/bin/env python3

import cv2
import imutils
import time
import numpy as np
from imutils.video.pivideostream import PiVideoStream
from datetime import datetime

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream(resolution = (1920, 1080)).start()
        self.flip = flip
        time.sleep(2.0)

    # def __del__(self):
    #     self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        now = datetime.now()
        cv2.putText(frame, "Secure-PI | {}".format(now), (10, 25), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def check_for_object(self, classifier):
        found_objects = False
        frame = self.flip_if_needed(self.vs.read()).copy() 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(objects) > 0:
            found_objects = True

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S").strip()
        cv2.putText(frame, "Secure-PI | {}".format(now), (10, 25), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(), found_objects)
