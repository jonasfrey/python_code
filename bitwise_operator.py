import time

for val in range(0,8*8):
    bin_num = 0b10010001
    time.sleep(0.08)
    bin_shifted_right = bin_num >> val%8
    bin_shifted_left = bin_num << val%8
    if int(val / 16) % 2 == 0: 
        print("shift right")
        print(str(bin(bin_num)[2:]) +">>"+ str(val%8) )
        print(str(bin(bin_shifted_right)[2:].zfill(8) ) + "")
    else: 
        print("shift left")
        print(str(bin(bin_num)[2:]) +"<<"+ str(val%8) )
        print(str(bin(bin_shifted_left)[2:].zfill(8) ) + "")


    
print('Does a "bitwise and". Each bit of the output is 1 if the corresponding bit of x AND of y is 1, otherwise it"s 0. ')
print("bitwise and")
print("(0b01010101 & 0b01010101)")
print(str(bin(0b01010101 & 0b01010101)[2:]).zfill(8))
print(" ")

print("bitwise and")
print("(0b01010101 & 0b10101010)")
print(str(bin(0b01010101 & 0b10101010)[2:]).zfill(8))
print(" ")

print("bitwise and")
print("(0b01010101 & 0b00001111)")
print(str(bin(0b01010101 & 0b00001111)[2:]).zfill(8))
print(" ")


print('Does a "bitwise or". Each bit of the output is 0 if the corresponding bit of x AND of y is 0, otherwise it"s 1. ')
print("bitwise or")
print("(0b01010101 | 0b01010101)")
print(str(bin(0b01010101 | 0b01010101)[2:]).zfill(8))
print(" ")

print("bitwise or")
print("(0b01010101 | 0b10101010)")
print(str(bin(0b01010101 | 0b10101010)[2:]).zfill(8))
print(" ")

print("bitwise or")
print("(0b01010101 | 0b00001111)")
print(str(bin(0b01010101 | 0b00001111)[2:]).zfill(8))
print(" ")


print('Returns the complement of x - the number you get by switching each 1 for a 0 and each 0 for a 1. This is the same as -x - 1. ')
print("tilde")
print("( ~ 0b01010101)")
print(str(bin( ~ 0b01010101)[2:]).zfill(8))
print(" ")

print("tilde")
print("( ~ 0b10101010)")
print(str(bin( ~ 0b10101010)[2:]).zfill(8))
print(" ")

print("tilde")
print("( ~ 0b00001111)")
print(str(bin( ~ 0b00001111)[2:]).zfill(8))
print(" ")


print('Does a "bitwise exclusive or". Each bit of the output is the same as the corresponding bit in x if that bit in y is 0, and it"s the complement of the bit in x if that bit in y is 1. ')
print("bitwise exclusive or")
print("(0b01010101 ^ 0b01010101)")
print(str(bin(0b01010101 ^ 0b01010101)[2:]).zfill(8))
print(" ")

print("bitwise exclusive or")
print("(0b01010101 ^ 0b10101010)")
print(str(bin(0b01010101 ^ 0b10101010)[2:]).zfill(8))
print(" ")

print("bitwise exclusive or")
print("(0b01010101 ^ 0b00001111)")
print(str(bin(0b01010101 ^ 0b00001111)[2:]).zfill(8))
print(" ")