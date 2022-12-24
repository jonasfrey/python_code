import cv2

vidcap = cv2.VideoCapture('animation.gif')
success,image = vidcap.read()
count = 0

n_images = 0
a_s_image = []
while success:
    n_images+=1
    a_img_resized = cv2.resize(image, dsize=(72, 40), interpolation=cv2.INTER_CUBIC)
    
    a_s_image_y = [] 
    for n_y in range(0, 40):
        a_s_image_x = []
        for n_x in range(0, 72):
            a_value = a_img_resized[n_y][n_x]
            if(a_value[0] > 128):
                a_s_image_x.append("1")
            else:
                a_s_image_x.append("0")
            
        s_image_x = ",".join(a_s_image_x)
        # print(s_image_x)
        a_s_image_y.append(s_image_x)
    s_image_y = "{\n"+ "},\n{".join(a_s_image_y) +"\n}\n"
    print(s_image_y)
    a_s_image.append(s_image_y)

    cv2.imwrite("frame%d.jpg" % count, a_img_resized)     # save frame as JPEG file      
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1


s_image = s_image_y = "{\n"+ "},\n{".join(a_s_image) +"\n}\n"
f = open("a_a_image.txt", "w")
s_image = "int a_a_img["+str(n_images)+"][40][72] = "+s_image+";"
f.write(s_image)
f.close()
print("done")



