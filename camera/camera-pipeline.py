import numpy as np  
import cv2 
import dlib
import math
from imutils import face_utils
import pyautogui
import time
import zmq
from threading import Thread, Event
from time import sleep
import signal
import sys
import queue

event = Event()

average_filter = [0]#the queue being used to keep track of the filtered angles so far.
cameraConnected = False#whether the camera is connected
debug = True#whether to print debug messages.

def debugPrint(msg):
    if debug:
        print(msg)

#function that is doing the webcam setup/opencv pipeline.
def process_webcam():
    global cameraConnected
    global average_filter
    PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"  
    RIGHT_EYE_POINTS = list(range(36, 42)) 
    LEFT_EYE_POINTS = list(range(42, 48))  
    #FULL_POINTS = list(range(0, 68))  
    #MOUTH_OUTLINE_POINTS = list(range(48, 61)) 
    while(True):
        #wait until a webcam is connected
        camera = cv2.VideoCapture(0)  
        if camera is None or not camera.isOpened():
            debugPrint("CAMERA PIPELINE: camera disconnected")
            cameraConnected = False
            sleep(3)
        else:
            debugPrint("CAMERA PIPELINE: camera connected")
            cameraConnected = True
            #start doing image processing on the camera. This should be able to run indefinetely,
            #unless the camera is disconnected.
            try:
                fps = camera.get(cv2.CAP_PROP_FPS)
                detector = dlib.get_frontal_face_detector()  
                predictor = dlib.shape_predictor(PREDICTOR_PATH)  
                filter_length = 2

                while(True):
                    ret, frame = camera.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    rects = detector(gray, 1)
                    for i, rect in enumerate(rects):
                        shape = predictor(gray, rect)
                        shape = face_utils.shape_to_np(shape)
                        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])  
                        #face_hull = cv2.convexHull(landmarks[FULL_POINTS])
                        #mouth_hull = cv2.convexHull(landmarks[MOUTH_OUTLINE_POINTS])
                        l_eye_hull = cv2.convexHull(landmarks[LEFT_EYE_POINTS])
                        r_eye_hull = cv2.convexHull(landmarks[RIGHT_EYE_POINTS])

                        #Consider left and right eyes as reference point of orientation of face
                        Ml = cv2.moments(l_eye_hull)
                        cXl = int(Ml["m10"] / Ml["m00"])
                        cYl = int(Ml["m01"] / Ml["m00"])
                        Mr = cv2.moments(r_eye_hull)
                        cXr = int(Mr["m10"] / Mr["m00"])
                        cYr = int(Mr["m01"] / Mr["m00"])

                        x = (cXl - cXr)
                        y = (cYl - cYr)
                        #calculate the angle from horizontal of the line between the center of the eyes.
                        rotation = -math.degrees(math.atan(y/x))

                        #Add to the average filter. Initially builds up members, then after he filter is full starts
                        if len(average_filter) <= filter_length:
                            average_filter.append(rotation)
                        else:
                            average_filter.pop(0)
                            average_filter.append(rotation)
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
                    #cv2.imshow('Frame',frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                # release camera/opencv windows
                camera.release()
                cv2.destroyAllWindows()
            except:
                pass

#main function
if __name__=="__main__":
    t = Thread(target=process_webcam)#the opencv thread
    t.start()

    #create the server that will send the camera values to unity
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    #until interrupted, do the request/response lifecycle.
    while True:
        #only send responses if the camera is connected.a
        while cameraConnected:
                message = socket.recv()
                if(message == b"a"):
                    socket.send(str(np.average(average_filter)).encode())
                else:
                    debugPrint("CAMERA SERVER: Unsupported Command received" + str(message))
                    socket.send(b"u")
    t.join()