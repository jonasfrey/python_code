import cv2
import threading
import time

class camThread(threading.Thread):
    def __init__(self, id, cameras):
        threading.Thread.__init__(self)
        self.id = id
        self.cameras = cameras

        print(self.cameras.frame1)

    def run(self):
        cam = cv2.VideoCapture(self.id)
        
        while rval:
            rval, frame = cam.read()
            cv2.imshow("asdf", frame)
            cameras_frame = setattr(self.cameras, "frame"+str(self.id), frame)

    cv2.destroyAllWindows()

# Create threads as follows
# frames = {
#     "cam1": None,
#     "cam1_data_changed": False,
#     "cam3":None,
#     "cam3_data_changed":False
#     }
# thread1 = camThread(1, frames)
# thread2 = camThread(3, frames)

# thread1.start()
# thread2.start()

class Cameras:
    def __init__(self):
        self._frame1 = None
        self.thread1 = camThread(1, self)
        self.thread1.start()
        
    @property 
    def frame1(self):
        return self._frame1

    @frame1.setter
    def frame1(self, value): 
        print("trying to set frame1 " +str(value))
        self._frame1 = value


cameras = Cameras()

while True:
    time.sleep(0.01)
    if cameras.frame1 != None:
        cv2.imshow("frameadfs1", cameras.frame1)


# while True: 

#     print(frames)    
#     time.sleep(0.01)
#     if(frames["cam1_data_changed"] == True):
#         cv2.imshow("cam1", frames["cam1"])
#         frames["cam1_data_changed"] = False

    

print("Active threads", threading.activeCount())

# import cv2
# import threading

# class camThread(threading.Thread):
#     def __init__(self, previewName, camID):
#         threading.Thread.__init__(self)
#         self.previewName = previewName
#         self.camID = camID
#     def run(self):
#         print "Starting " + self.previewName
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
# thread2 = camThread("Camera 2", 2)
# thread1.start()
# thread2.start()