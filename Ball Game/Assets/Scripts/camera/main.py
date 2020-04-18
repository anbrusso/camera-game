from debug import *
from feed import CameraFeed as feed
from pipeline import ImagePipeline as pipeline
import zmq
import cv2
from threading import Thread, Event
import traceback
import datetime

#main function
if __name__=="__main__":
    set_debug(False)
    log("Camera Server started")
    #create the server that will send the camera values to unity
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")#use the loopback address only
    cf = feed().start()
    pipe = pipeline(cf,2).start()

    while True:
        if cf.detected().isSet():
            message = socket.recv()
            if(message == b"a"):
                log(pipe.get_angle())
                socket.send(str(pipe.get_angle()).encode())
            else:
                socket.send(b"u")
            #frame = cf.read()
            #cv2.imshow('Frame',frame)
            #key = cv2.waitKey(1) & 0xFF
    cf.kill()
    pipe.kill()
    cv2.destroyAllWindows()    
