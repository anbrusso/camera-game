from threading import Thread, Event
from time import sleep
import cv2
from debug import *
#Threaded camera feed that buffers in each frame, instead of blocking reads (I/O is slow)
class CameraFeed:
    def __init__(self, camera_num = 0, name = "CameraFeed"):
            self.feed = cv2.VideoCapture(camera_num)
            self.is_detected = Event()#event to tell threads waiting for a camera when it is available.
            #try to read an initial frame
            ret, self.frame = self.feed.read() 
            self.name = name
            self.camera_num = camera_num
            self.alive = True
    def start(self):
        thread = Thread(target=self.__detect, name = self.name)
        thread.start()
        return self
    def __detect(self):
        while(self.alive):
            self.feed = cv2.VideoCapture(self.camera_num)
            #are we connected to the camera? If not try reopening
            if self.feed is None or not self.feed.isOpened():
                log("Camera Disconnected")
                self.is_detected.clear()
                sleep(3)#wait a bit to reconnect, just so we aren't constantly polling.
            else:
                self.is_detected.set()
                log("Camera Connected")
                #if the camera disconnects, we won't be able to read anymore (exception), so we return to polling
                try:
                    while(self.alive):
                        ret, self.frame = self.feed.read()
                        #log("Frame")
                        if self.frame is None:
                            break
                except:
                    pass
    def read(self):
        return self.frame
    def detected(self):
        return self.is_detected
    def kill(self):
        self.feed.release()
        self.is_detected.set()#release other threads waiting on the camera... Otherwise they will block forever.
        self.alive = False