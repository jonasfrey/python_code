import cv2

cam = cv2.VideoCapture(5)

while True:
    check, frame = cam.read()

    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()