from threading import Thread
import cv2, time

class VideoStreamWidget(object):
    def __init__(self, src=1):
        self.src = src
        self.this_ts = 0
        self.last_ts = 0
        self.delta_ts = 0
        self.capture = cv2.VideoCapture(self.src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                self.this_ts = round(time.time() * 1000)
                self.delta_ts = abs(self.this_ts - self.last_ts)
                self.last_ts = self.this_ts
                print('frame fps: '+str(1000/self.delta_ts))
            time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        cv2.imshow('frame'+str(self.src), self.frame)


        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget(1)
    video_stream_widget2 = VideoStreamWidget(3)
    while True:
        try:
            video_stream_widget.show_frame()
            video_stream_widget2.show_frame()
        except AttributeError:
            pass
