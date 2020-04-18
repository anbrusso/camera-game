from threading import Thread
import cv2
import dlib
import numpy as np  
import math
import os
from debug import *
#Threaded Camera feed that buffers in each frame, instead of blocking reads (I/O is slow)
class ImagePipeline:
    def __init__(self, cf, filter_length =2,name = "ImagePipeline"):
            self.name = name
            self.alive = True
            self.filter_length = filter_length#ho w
            self.cf = cf
            self.average_filter =[0]
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
    def is_blinking(self):
        return self.eyes_closed

    def __get_head_angle(self,l_hull,r_hull):
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
    def __get_eyes_closed(self,l_hull,r_hull):
        return False
        #print("Filter" + str(np.average(average_filter)))
        #if(Ml["m00"]
        #x,y,w,h = cv2.boundingRect(l_eye_hull)
        #l_ratio = float(w)/h
        #x,y,w,h = cv2.boundingRect(r_eye_hull)
        #r_ratio = float(w)/h
        #eye_aspect = (l_ratio + r_ratio) / 2.0
        #if(eye_aspect < 4):
        #    print("eyes open" + str(eye_aspect))
        #else:
        #    print("eyes closed" + str(eye_aspect))
    def kill(self):
        self.alive = False