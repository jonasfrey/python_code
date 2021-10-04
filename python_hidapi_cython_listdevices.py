import hid

device_list = hid.enumerate()
print(device_list)

for val in device_list:
    print(val)
