import numpy as np
import cv2

img = np.zeros((512,512,3), np.uint8)

font                   = cv2.FONT_HERSHEY_SIMPLEX
position               = (10,500)
fontScale              = 2
fontColor              = (255,255,0)

cv2.putText(img,'Hello World!',
    position,
    font,
    fontScale,
    fontColor)

cv2.imshow("img",img)
cv2.waitKey(0)