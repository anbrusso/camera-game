from threading import Thread, Event
from time import sleep
import cv2
from debug import *
#Threaded camera feed that buffers in each frame, instead of blocking reads (I/O is slow)
class CameraFeed:
    def __init__(self, camera_num = 0, name = "CameraFeed"):
            self.camera_num = camera_num#for our purposes, we only have one camera, so this is just 0
            self.feed = self.__open_camera()
            self.is_detected = Event()#event to tell other threads waiting for a camera when it is available.

            #try to read an initial frame
            ret, self.frame = self.feed.read() 
            self.name = name
            self.alive = True

    def __open_camera(self):
        """ Opens the camera feed, and sets its resolution (400x300) """
        cap =cv2.VideoCapture(self.camera_num)
        cap.set(3,400)
        cap.set(4,300)
        return cap
    
    def start(self):
        """Called to start the thread."""
        thread = Thread(target=self.__detect, name = self.name)
        thread.start()
        return self

    def __detect(self):
        """ Primary entry point for this thread. Maintains the isdetected variable for others, and also reads in new frames from the camera as they are available."""
        while(self.alive):
            self.feed = self.__open_camera()
            #are we connected to the camera? If not try reopening
            if self.feed is None or not self.feed.isOpened():
                log("Camera Disconnected")
                self.is_detected.clear()
                sleep(1)#wait a bit to reconnect, just so we aren't constantly polling.
            else:
                self.is_detected.set()
                log("Camera Connected")
                #if the camera disconnects, we won't be able to read anymore (exception), so we return to polling
                try:
                    while(self.alive):
                        ret, frame = self.feed.read()
                        if frame is None:
                            break
                        self.frame = frame
                        log("Frame")
                except:
                    pass

    def read(self):
        """ Read the currently buffered frame from the camera """
        return self.frame

    def detected(self):
        """An event object for wheter a camera is available. Others can call and wait on this object, to pause when camera isn't available."""
        return self.is_detected

    def kill(self):
        """Called to stop the thread."""
        self.feed.release()
        self.is_detected.set()#release other threads waiting on the camera... Otherwise they will block forever.
        self.alive = False