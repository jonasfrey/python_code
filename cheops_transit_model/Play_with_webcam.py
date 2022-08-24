""""
Baptiste Lavie
May 2022
NCCR PlanetS https://nccr-planets.ch/
"""
import cv2
from timeit import default_timer as timer
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import matplotlib.animation as animation

###### param
resizeWidth = 500 ## pour redimensionner la webcam
What_webcam = 5 ### an integer - it depends on the computer, start with 0 then 1 etc. until you get the webcam you want
###### Le rectangle surlequel la lumière est intégré :
### L'origine est en haut à gauche sur la fenetre de la webcam opencv
point_haut = (300,170)
point_bas = (220,120) #### point en haut à gauche
####
Time_window = 50 ### en seconde fenetre observation (le plot se remet a zero)
########################################
#### find the source ####################
def find_the_source(gray):
    threshold_autour_du_Max = 0.99 ## %
    radius = 31
    color = (255, 255, 255)
    ######## locate light center
    gray_blur = cv2.GaussianBlur(gray, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_blur)
    center_coordinates = maxLoc
    ### take pixels around the max
    ret, thresh1 = cv2.threshold(gray_blur, maxVal *threshold_autour_du_Max, 255, cv2.THRESH_BINARY)
    light_source_idx = np.zeros(gray.shape,dtype = np.bool)
    for row in range(gray.shape[0]):
        for col in range(gray.shape[1]):
            if thresh1[row,col] == 255:
                light_source_idx[row,col] = True
    return light_source_idx

def make_labels_plot():
    plt.title('Lightcurve')
    plt.xlabel("Time [seconds]")
    plt.ylabel("Flux (quantity of light) [Normalized]")
    plt.xlim(0, Time_window)
    plt.ylim(0.5, 1.5)

capture = cv2.VideoCapture(What_webcam)

 
###########################
###########################
plt.ion()
# Initialize plot.
fig, ax = plt.subplots()
make_labels_plot()
# Initialize plot line object(s). Turn on interactive plotting and show plot.
lw = 3
alpha = 0.5
lineGray = ax
x, y = [0],[1]
lc, = lineGray.plot(x,y,color = 'k') #,ms = 5,color = 'k',marker = 'o')
plt.draw()
#################
start = timer() #### start the timer
previous_time = 0
counter = 0
####Grab, process, and display video frames. Update plot line object(s).
while True :
    (grabbed, frame) = capture.read()
    if not grabbed:
        break
######Resize frame to width, if specified.
    if resizeWidth > 0:
        (height, width) = frame.shape[:2]
        resizeHeight = int(float(resizeWidth / width) * height)
        frame = cv2.resize(frame, (resizeWidth, resizeHeight),
            interpolation=cv2.INTER_AREA)
    # Normalize histograms based on number of pixels per frame.
#    numPixels = np.prod(frame.shape[:2])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray, point_bas, point_haut, (255, 0, 0), 5)
#    light_source_idx = find_the_source(gray)
    cv2.imshow('Grayscale', gray)
#    ####
#    light_value = np.sum(gray[light_source_idx])
#    light_value = np.sum(gray[light_source_idx])
    light_value = np.sum(gray[point_bas[1]:point_haut[1],point_bas[0]:point_haut[0]])
    try:
        flux_norm +1
    except:
        flux_norm = light_value * 1.
    now = timer()-start
    ###### print fps
#    if now - previous_time > 1:
#        print(now,"fps",counter)
#        previous_time = 0
#        counter = 0
#        previous_time  = now * 1.
    ######## plot here
#    print(now,light_value)
    x.append(now)
    y.append(light_value / flux_norm)
    lc.set_data(x,y)
#    plt.plot(x,y,color = 'k')
    #ms = 5,color = 'k',marker = 'o')
#    fig.canvas.draw_idle()
    plt.pause(0.00001)
#    fig.canvas.draw_idle()
    if timer()-start > Time_window:
        start = timer()
        previous_time = 0
        plt.clf()
        x, y = [0],[1]
        lc, = plt.plot(x,y,color = 'k')
        make_labels_plot()
        plt.pause(0.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    counter += 1
    
capture.release()
cv2.destroyAllWindows()

#
#





