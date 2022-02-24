# list devices 
# pip install pyusb 
# pip3 install pyusb
import usb.core
import sys
import time
#Bus 001 Device 004: ID 09e8:0028 AKAI  Professional M.I. Corp. APC MINI

vendor_id = 0x09e8
product_id = 0x0028

device=usb.core.find(idVendor=vendor_id,idProduct=product_id)
# print(device[0])
interface = device[0].interfaces()[1]

end_point = interface.endpoints()[1]
i=interface.bInterfaceNumber
device.reset()

if device.is_kernel_driver_active(i):
    try:
        device.detach_kernel_driver(i)
    except usb.core.USBError as e:
        sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))

# device.set_configuration()
endpoint_address = end_point.bEndpointAddress 

# endpoint_address is a literal byte stream

try: 
    for i in range(0,64):
        time.sleep(0.01)
        msg = [0x09, 0x90, i, i]
        print(msg)
        device.write(1, msg)
        # device.write(1, 'suckablyad')
except: 
    print("error writing to device")

def reading_loop():
    timout_time = 1000
    try: 
        while(True):

            try:
                r=device.read(endpoint_address, end_point.wMaxPacketSize, timout_time)
                print(r)
            except: 
                print('no bytes received')

    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

    # for i in range(0,10):
    #     print(i)
    #     device.read(endpoint_address, end_point.wMaxPacketSize, timout_time)
    #     # print(r)
    #     print(len(r))
