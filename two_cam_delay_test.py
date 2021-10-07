import cv2
import pyautogui
import time
import colorsys
from tkinter import * 
import numpy as np

import threading


# no multithreading , one camera has delay 
# #capture = cv2.VideoCapture("http://11.23.58.105:8080/video")
# #capture = cv2.VideoCapture("http://11.23.58.102:8080/video")
# capture1 = cv2.VideoCapture(1)
# capture2 = cv2.VideoCapture(3)

# capture1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
# capture1.set(cv2.CAP_PROP_EXPOSURE, 1)

# capture2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 8)
# capture2.set(cv2.CAP_PROP_EXPOSURE, 8)

# while(True):

#     _, frame1 = capture1.read()
#     _, frame2 = capture2.read()
#     cv2.imshow("frame1", frame1)
#     cv2.imshow("frame2", frame2)

#     if(cv2.waitKey(1) == ord("q")):
#         break

# capture1.release()
# capture2.release()

# class camThread(threading.Thread):
#     def __init__(self, previewName, camID):
#         threading.Thread.__init__(self)
#         self.previewName = previewName
#         self.camID = camID
#     def run(self):
#         print ("Starting " + self.previewName)
#         camPreview(self.previewName, self.camID)

# def camPreview(previewName, camID):
#     cv2.namedWindow(previewName)
#     cam = cv2.VideoCapture(camID)
#     if cam.isOpened():  # try to get the first frame
#         rval, frame = cam.read()
#     else:
#         rval = False

#     while rval:
#         cv2.imshow(previewName, frame)
#         rval, frame = cam.read()
#         key = cv2.waitKey(20)
#         if key == 27:  # exit on ESC
#             break
#     cv2.destroyWindow(previewName)

# # Create two threads as follows
# thread1 = camThread("Camera 1", 1)
# thread2 = camThread("Camera 3", 3)

# thread1.start()
# thread2.start()


#!/usr/bin/python3

import _thread
import time
import cv2

# capture1 = cv2.VideoCapture(1)
# capture2 = cv2.VideoCapture(3)

# capture1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
# capture1.set(cv2.CAP_PROP_EXPOSURE, 1)

# capture2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 8)
# capture2.set(cv2.CAP_PROP_EXPOSURE, 8)

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

def capture_and_im_show(capture, id):
    while(True):
        _, frame = capture.read()
        cv2.imshow("frame"+str(id), capture)

        if(cv2.waitKey(1) == ord("q")):
            break

def start_video_capture(id): 
    capture = cv2.VideoCapture(id)
    while(True):

        _, frame = capture.read()
        cv2.imshow("frame"+str(id), frame)

        if(cv2.waitKey(1) == ord("q")):
            break

    capture.release()

    
# Create two threads as follows
try:
    _thread.start_new_thread( start_video_capture,(1,))
    _thread.start_new_thread( start_video_capture,(3,))
except ValueError:
    print(ValueError)
    print ("Error: unable to start thread")

while 1:
   pass
