import cv2
import pyautogui

#capture = cv2.VideoCapture("http://11.23.58.105:8080/video")
#capture = cv2.VideoCapture("http://11.23.58.102:8080/video")
capture = cv2.VideoCapture(1)
capture2 = cv2.VideoCapture(3)


while(True):
    _, frame = capture.read()
    _, frame2 = capture2.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsl = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)


    #h s v -> hue saturation value
    # 0-1 -> mapped to 0->2^8 => 0-255
    # h->hue 0-1 (red-via blue-red)
    # s->saturation 0-1 
    #   if value==1 &&  saturation == 0
    #       result == white
    #   if value==1 && saturation == 1 
    #       result == full color
    #   if value==0.5 && saturation == 1
    #       result == full color
    #   if value==0.5 && saturation == 0.5 
    #       result == grayish color
    # v->value-> 0-1 
    #   if saturation == 0
    #       0-1 (black to white)
    #   if saturation == 1 
    #       0-1 (black to full color)

    # hue_plus_minus = 1/20 # plus minus 1/10 of circle
    # low_h = (1/3) - hue_plus_minus # green starts at a third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    # low_s = 0 # we want full saturation 
    # low_v = (7/8) # we start at 1/8 , very dark color almost black
    
    # high_h = (1/3) + hue_plus_minus # green ends at 120 plus certain degrees
    # high_s = 0.5 # we want full saturation 
    # high_v = (8/8) # we end at 8/8 ,so full color green

    # blue ps motion controller
    # low_h = (2/3-(1/10)) - hue_plus_minus # blue starts at two third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    # low_s = 0.2 # we want full saturation 
    # low_v = (2/8) # we start at 1/8 , very dark color almost black
    
    # high_h = (2/3-(1/10)) + hue_plus_minus # blue ends at 240 plus certain degrees
    # high_s = 1 # we want full saturation 
    # high_v = (8/8) # we end at 8/8 ,so full color green


    # blue arduino led 
    hue_plus_minus = 1/20 # plus minus 1/10 of circle

    low_h = (2/3-(1/10)) - hue_plus_minus # blue starts at two third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    low_s = 0 # we want full saturation 
    low_v = 0.9 # we start at 1/8 , very dark color almost black
    
    high_h = (2/3-(1/10)) + hue_plus_minus # blue ends at 240 plus certain degrees
    high_s = 0.05 # we want full saturation 
    high_v = 1 # we end at 8/8 ,so full color green

    low_h = (2/3-(1/10)) - hue_plus_minus # blue starts at two third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    low_s = 0 # we want full saturation 
    low_v = 1 # we start at 1/8 , very dark color almost black
    
    high_h = (2/3-(1/10)) + hue_plus_minus # blue ends at 240 plus certain degrees
    #high_s = 0.2 # we want full saturation 
    high_v = 1 # we end at 8/8 ,so full color green
    high_s = (pyautogui.position()[0]) / 1920; 

    unnormalized_max_h = 180
    unnormalized_max_s = 255
    unnormalized_max_v = 255
    mask = cv2.inRange(
        hsv,
            (
            unnormalized_max_h * low_h,
            unnormalized_max_s * low_s,
            unnormalized_max_v * low_v
            ),
            (
            unnormalized_max_h * high_h,
            unnormalized_max_s * high_s,
            unnormalized_max_v * high_v
            )
        )
    

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    cv2.circle(frame, maxLoc, 5, (255, 0, 0), 2)
    # display the results of the naive attempt
    cv2.imshow("Naive", frame)


    # gray = cv2.GaussianBlur(gray, (2, 2), 0)
    # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # cv2.circle(frame, maxLoc, 2, (255, 0, 0), 2)
    # cv2.imshow("Robust", frame)

    # hue_plus_minus = 1/10 # plus minus 1/10 of circle
    # hue_start = (pyautogui.position()[0]) / 1920; 
    # hue_plus_minus = (pyautogui.position()[1]) / 1080; 
    # low_h = hue_start - hue_plus_minus # green starts at a third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    # low_s = 0 # we want full saturation 
    # low_l = (0.5) # we start at 1/8 , very dark color almost black
    
    # high_h = hue_start + hue_plus_minus # green ends at 120 plus certain degrees
    # high_s = 1 # we want full saturation 
    # high_l = (1) # we end at 8/8 ,so full color green

    # unnormalized_max_h = 180
    # unnormalized_max_s = 255
    # unnormalized_max_l = 255
    # mask = cv2.inRange(
    # hsl,
    #     (
    #     unnormalized_max_h * low_h,
    #     unnormalized_max_s * low_s,
    #     unnormalized_max_v * low_v
    #     ),
    #     (
    #     unnormalized_max_h * high_h,
    #     unnormalized_max_s * high_s,
    #     unnormalized_max_v * high_v
    #     )
    # )
    
    cv2.imshow('test_window_name', mask)
    cv2.imshow('test_window_name_frame', frame)
    cv2.imshow('test_window_name_frame2', frame2)
    if(cv2.waitKey(1) == ord("q")):
        break

capture.release()
cv2.destroyAllWindows()
