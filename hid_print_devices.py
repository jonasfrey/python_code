import hid
import time
import os


# for d in hid.enumerate():
#     keys = list(d.keys())
#     keys.sort()
#     for key in keys:
#         print("%s : %s" % (key, d[key]))
#     print()

### enumerate USB devices
for d in hid.enumerate():
    keys = list(d.keys())
    keys.sort()
    for key in keys:
        print("%s : %s" % (key, d[key]))
    print()
    
# def get_bar_string(value, max, width = 255):
#   value = int(value)
#   str_str = ""
#   perc = 1 / ((max+1) / (value+1))

#   for i in range(0, width):
#     if(i < width*perc):
#       str_str += "■"
#     else:
#       str_str += " " 
    
  

#   return str(value).rjust(len(str(max)), " ") + " | "+ str(hex(value)[2:]).rjust(len(str(hex(max)[2:])), " ") + " | " + str(bin(value)[2:]).rjust(len(str(bin(max)[2:])), "0") +  " ["+str_str+"]"

# print("Opening the device")

# # usb microscope cam a16f:0304

# VENDOR_ID = 0xa16f  
# PRODUCT_ID = 0X0304

# device = hid.device()
# device.open(VENDOR_ID, PRODUCT_ID)

# print("Manufacturer: %s" % device.get_manufacturer_string())
# print("Product: %s" % device.get_product_string())
# print("Serial No: %s" % device.get_serial_number_string())

# try:
#     while True:
#         d = device.read(64)
#         time.sleep(0.1)
#         if d:
#             #print("".join(["\n"]*10))
#             str_str = ""
#             for key,val in enumerate(d):
#                 str_str += ("indx "+str(key).rjust(2, " ")+": "+get_bar_string(val, 255, 255)) + "\n"
#             os.system('cls' if os.name == 'nt' else 'clear')
#             print(str_str)
#             #print('read: "{}"'.format(d))
# finally:
#     print("Closing the device")
#     device.close()




