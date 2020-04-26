from debug import *
from feed import CameraFeed as feed
from pipeline import ImagePipeline as pipeline
import zmq
import cv2
from threading import Thread, Event
import traceback
import datetime
import argparse


#main code entry point
if __name__=="__main__":
    #add the debug argument, so we can start in debug mode by running with --debug
    parser = argparse.ArgumentParser(description='Start image processing pipeline.')
    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--debug', dest='debug', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    #start in debugging mode, which doesn't wait for the camera client to connect
    if args.debug:
        set_debug(True)#will perform debug logging.
        cf = feed().start()
        pipe = pipeline(cf,3).start()

        #read frames, and print out the image from the pipeline.
        while True:
            if cf.detected().isSet():
                frame = cf.read()
                cv2.putText(frame,"Angle: " + str(pipe.get_angle()), (5,40), cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
                cv2.putText(frame,"Eyes Closed: " + str(pipe.is_closed()), (5,60), cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
                cv2.drawContours(frame,pipe.get_landmarks(),-1,(0,255,0),3)
                cv2.imshow('Debug',frame)
                key = cv2.waitKey(1) & 0xFF
    #starting in regular mode, need to start the server..
    else:
        set_debug(False)
        cf = feed().start()
        pipe = pipeline(cf,3).start()
        print("Camera Server started")
        while True:
            #in try block so that we ignore exceptions and just restart the server.
            try:
                #create the server that will send the camera values to unity
                context = zmq.Context()
                socket = context.socket(zmq.REP)
                socket.bind("tcp://127.0.0.1:5555")#use the loopback address only

                while True:
                    #only send responses if the camera is connected via usb, otherwise we don't have any data to send.
                    if cf.detected().isSet():
                        message = socket.recv()
                        if(message == b"a"):
                            log(pipe.get_angle())
                            socket.send(str(pipe.get_angle()).encode())
                        elif(message == b"e"):
                            log(pipe.is_closed())
                            socket.send(str(pipe.is_closed()).encode())
                        else:
                            socket.send(b"u")
                        frame = cf.read()
                        cv2.imshow('Frame',frame)
                        key = cv2.waitKey(1) & 0xFF
            except:
                pass
        #cleanup after ourselves.
        cf.kill()
        pipe.kill()
    cv2.destroyAllWindows()