import hid

# Bus 003 Device 002: ID 0c45:6368 Microdia  ACR010 USB Webcam
# Bus 003 Device 007: ID 1e7d:2dd2 ROCCAT  ACR010 USB Webcam

vendor_product = "0c45:6368"


parts = vendor_product.split(":")
vendor_string_hex = "0x"+parts[0]
product_string_hex = "0x"+parts[1]

vendor_string_int = int(vendor_string_hex, 16)
vendor_string_hex_value = hex(vendor_string_int)

product_string_int = int(product_string_hex, 16)
product_string_hex_value = hex(product_string_int)

print(str(hid.enumerate()).replace(",", "\n"))

with hid.device(vendor_string_int, product_string_int) as h:
	print(f'Device manufacturer: {h.manufacturer}')
	print(f'Product: {h.product}')
	print(f'Serial Number: {h.serial}')

# device.open(vendor_string_int, product_string_int)

# while True:
#     data = device.read(64)
#     if data:
#         print('read: "{}"'.format(data))

# device.close()