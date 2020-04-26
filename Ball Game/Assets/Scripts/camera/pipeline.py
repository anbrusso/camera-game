from threading import Thread
import cv2
import dlib
import numpy as np  
import math
import os
from debug import *
#Threaded image pipeline, takes in the camera feed as a parameter, and while the feed is open it processes available frames.
class ImagePipeline:
    """And image pipeline thread. Receives information from a CameraFeed, processes it, and makes available processed output values"""
    def __init__(self, cf, filter_length =2,name = "ImagePipeline"):
            self.name = name
            self.alive = True
            self.cf = cf
            self.filter_length = filter_length#how long the average filter will be for head angle
            self.average_filter =[0]
            self.eye_buffer =[False]#for the eyes, we keep a buffer of previous states, since we need to differentiate closed eyes from blinking.
            self.eye_buffer_length =20#buffer length found via guess and check
            self.eye_threshold =2.95#threshold found via guess and check.
            self.landmarks = []#useful for debugging. The landmark points

    def start(self):
        """Called to start the thread."""
        thread = Thread(target=self.__process_cf,name = self.name)
        thread.start()
        return self
        
    def __process_cf(self):
        """ The primary processing entry point. This is where we do our prediction, generate our outputs, and make them available to other threads requesting them."""
        log("Processing started")
        dirname = os.path.dirname(__file__)
        predictor_file = os.path.join(dirname,"shape_predictor_68_face_landmarks.dat")#shape prediction file built into the dlib library (from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
        r_eye = list(range(36, 42))#landmarks corresponding to the right eye
        l_eye = list(range(42, 48))#landmarks corresponding to the left eye

        detector = dlib.get_frontal_face_detector()  
        predictor = dlib.shape_predictor(predictor_file)
        while(self.alive):
            self.cf.detected().wait()#camera needs to be connected, otherwise we're wasting resources. This will block if no camera.
            #grab frame if available
            frame = self.cf.read()
            if frame is None:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#grayscale helps reduce noise

            rects = detector(gray, 1)
            for i, rect in enumerate(rects):
                landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()]) #get our landmarks out.
                self.landmarks =landmarks

                #eye hulls, which we'll be using for our math
                l_eye_hull = cv2.convexHull(landmarks[l_eye])
                r_eye_hull = cv2.convexHull(landmarks[r_eye])

                #compute head angle, add to average filter.
                angle = self.__get_head_angle(l_eye_hull,r_eye_hull)
                #check if eyes are closed
                eye_aspect = self.__get_eye_aspect(l_eye_hull,r_eye_hull)

                #Add angle to our averaging filter
                if len(self.average_filter) <= self.filter_length:
                    self.average_filter.append(angle)
                else:
                    self.average_filter.pop(0)
                    self.average_filter.append(angle)
            
                #we keep a buffer for the eye aspects, so we know what happened in the past
                if len(self.eye_buffer) <= self.eye_buffer_length:
                    self.eye_buffer.append(eye_aspect > self.eye_threshold)#add whether eye was closed/open to buffer.
                else:
                    self.eye_buffer.pop(0)
                    self.eye_buffer.append(eye_aspect > self.eye_threshold)

    def get_angle(self):
        """Getter, which returns the angle of the player's head"""
        return np.average(self.average_filter)

    def is_closed(self):
        """Getter, which returns whether the person's eye is currently (within the buffer length) closed"""
        time_closed = sum(self.eye_buffer)#of our buffer, how often were the eyes closed?

        #if over threshold 10 times in a row, consider eyes closed. 10 was found through guess and check
        if(time_closed > 10):
            return True
        else:
            return False

    def get_landmarks(self):
        """ Used for debugging, to make the landmarks available for printing on the image"""
        return self.landmarks

    def __get_head_angle(self,l_hull,r_hull):
        """Performs the calculations necessary to find the angle of the person's head from horizontal."""
        try:
            #Consider left and right eyes as reference point of orientation of face
            Ml = cv2.moments(l_hull)#left moment
            #center of left eye
            cXl = int(Ml["m10"] / Ml["m00"])
            cYl = int(Ml["m01"] / Ml["m00"])
            #center of right eye
            Mr = cv2.moments(r_hull)#right moment
            cXr = int(Mr["m10"] / Mr["m00"])
            cYr = int(Mr["m01"] / Mr["m00"])

            #directional vector between the eyes
            x = (cXl - cXr)
            y = (cYl - cYr)

            #calculate the angle from horizontal of the line between the center of the eyes.
            if x == 0:#division by zero
                return 180
            return -math.degrees(math.atan(y/x))
        except:
            return 180

    def __get_eye_aspect(self,l_hull,r_hull):
        """Performs the calculations to get the aspect ratio of the person's head. Averages between the eyes."""
        try:
            x,y,w,h = cv2.boundingRect(l_hull)
            l_ratio = float(w)/h#aspect ratio of the left eye
            x,y,w,h = cv2.boundingRect(r_hull)
            r_ratio = float(w)/h#aspect ratio of right eye

            eye_aspect = (l_ratio + r_ratio) / 2.0#use the average of the eye's aspects, to hopefully help account for if they are turned.
            return eye_aspect
        except:
            return 2.0
            
    def kill(self):
        """Called to stop the thread."""
        self.alive = False