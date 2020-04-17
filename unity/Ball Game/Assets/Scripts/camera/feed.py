from threading import Thread, Event
from time import sleep
import cv2
#Threaded Camera feed that buffers in each frame, instead of blocking reads (I/O is slow)
class CameraFeed:
    def __init__(self, camera_num = 0, name = "CameraFeed"):
            self.feed = cv2.VideoCapture(camera_num)
            self.detected = Event()#event to tell threads waiting for a camera when it is available.
            #try to read an initial frame
            try: 
                ret, self.frame = self.feed.read() 
                self.detected.set()
            except:
                self.detected.clear()
            self.name = name
            self.camera_num = camera_num
            self.alive = True
    def start(self):
        thread = Thread(target=self.detect)
        thread.start()
    def __detect(self):
        while(self.alive):
            #are we connected to the camera? If not try reopening
            if self.feed is None or not self.feed.isOpened():
                self.feed = cv2.VideoCapture(self.camera_num)
                self.detected.set()
                sleep(3)#wait a bit to reconnect, just so we aren't constantly polling.
            else:
                self.detected.clear()
                #if the camera disconnects, we won't be able to read anymore, so we return to pollying
                try:
                    while(self.Alive):
                        ret, self.frame = self.feed.read()
                except:
                    pass
    def read(self):
        return self.frame
    def detected(self):
        return self.detected
    def kill(self):
        self.feed.release()
        self.detected.set()#release other threads waiting on the camera... Otherwise they will block forever.
        self.alive = False