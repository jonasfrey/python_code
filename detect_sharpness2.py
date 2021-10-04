
import cv2
 
def getImageVar(imgPath):
    image = cv2.imread(imgPath)
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar
 
imageVar = getImageVar("./sharp.jpg")
print("sharpness ./sharp.jpg")
print(imageVar)


 
imageVar = getImageVar("./not_sharp.jpg")
print("sharpness ./not_sharp.jpg")
print(imageVar)



 
imageVar = getImageVar("./blurred.jpeg")
print("sharpness ./blurred.jpeg")
print(imageVar)


