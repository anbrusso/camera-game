from threading import Thread
import cv2
import dlib
import numpy as np  
import math
import os
from debug import *
#Threaded image pipeline, takes in the camera feed as a parameter, and while the feed is open it processes available frames.
class ImagePipeline:
    def __init__(self, cf, filter_length =2,name = "ImagePipeline"):
            self.name = name
            self.alive = True
            self.filter_length = filter_length#ho w
            self.cf = cf
            self.average_filter =[0]
            self.eye_buffer =[0]
            self.eye_buffer_length =20
            self.eye_threshold =2.95
            self.eyes_closed = False
    def start(self):
        thread = Thread(target=self.__process_cf,name = self.name)
        thread.start()
        return self
    #where them main image processing is happening
    def __process_cf(self):
        log("Processing started")
        dirname = os.path.dirname(__file__)
        predictor_file = os.path.join(dirname,"shape_predictor_68_face_landmarks.dat")
        r_eye = list(range(36, 42)) 
        l_eye = list(range(42, 48))
        detector = dlib.get_frontal_face_detector()  
        predictor = dlib.shape_predictor(predictor_file)
        while(self.alive):
            #camera needs to be connected, otherwise we're wasting resources.
            self.cf.detected().wait()
            frame = self.cf.read()
            if frame is None:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#grayscale helps reduce noise
            rects = detector(gray, 1)
            for i, rect in enumerate(rects):
                landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])  
                l_eye_hull = cv2.convexHull(landmarks[l_eye])
                r_eye_hull = cv2.convexHull(landmarks[r_eye])

                #compute head angle, add to average filter.
                angle = self.__get_head_angle(l_eye_hull,r_eye_hull)
                if len(self.average_filter) <= self.filter_length:
                    self.average_filter.append(angle)
                else:
                    self.average_filter.pop(0)
                    self.average_filter.append(angle)
                
                #check if eyes are closed
                eyes_closed = self.__get_eyes_closed(l_eye_hull,r_eye_hull)
    def get_angle(self):
        return np.average(self.average_filter)
    def is_closed(self):
        return self.eyes_closed

    def __get_head_angle(self,l_hull,r_hull):
        try:
            #Consider left and right eyes as reference point of orientation of face
            Ml = cv2.moments(l_hull)#left moment
            cXl = int(Ml["m10"] / Ml["m00"])
            cYl = int(Ml["m01"] / Ml["m00"])
            Mr = cv2.moments(r_hull)#right moment
            cXr = int(Mr["m10"] / Mr["m00"])
            cYr = int(Mr["m01"] / Mr["m00"])

            x = (cXl - cXr)
            y = (cYl - cYr)
            #log(str(x)+", "+str(y))
            #calculate the angle from horizontal of the line between the center of the eyes.
            if x == 0:
                return 180
            return -math.degrees(math.atan(y/x))
        except:
            return 180
    def __get_eyes_closed(self,l_hull,r_hull):
        #print("Filter" + str(np.average(average_filter)))
        #if(Ml["m00"]
        try:
            x,y,w,h = cv2.boundingRect(l_hull)
            l_ratio = float(w)/h
            x,y,w,h = cv2.boundingRect(r_hull)
            r_ratio = float(w)/h
            eye_aspect = (l_ratio + r_ratio) / 2.0
            
            #we keep a buffer so we know what happened before now
            if len(self.eye_buffer) <= self.eye_buffer_length:
                self.eye_buffer.append(eye_aspect)
            else:
                self.eye_buffer.pop(0)
                self.eye_buffer.append(eye_aspect)
            array = np.array(self.eye_buffer)
            time_closed = (array > self.eye_threshold).sum()

            #if over threshold 5 times in a row, consider eyes closed
            if(time_closed > 10):
                self.eyes_closed = True
            else:
                self.eyes_closed = False
        except:
            self.eyes_closed = False
    def kill(self):
        self.alive = False