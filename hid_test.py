import hid

VENDOR_ID = 0x054c  # Sony dualshok 4    
PRODUCT_ID = 0x05c4 # ADU200 Device product name - change this to match your product

device = hid.device()
device.open(VENDOR_ID, PRODUCT_ID)
print('Connected to ADU{}\n'.format(PRODUCT_ID))

