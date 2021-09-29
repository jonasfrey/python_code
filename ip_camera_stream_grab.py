import cv2

capture = cv2.VideoCapture("http://11.23.58.105:8080/video")


while(True):
    _, frame = capture.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
    
    cv2.imshow('test_window_name', mask)

    if(cv2.waitKey(1) == ord("q")):
        break

capture.release()
cv2.destroyAllWindows()
