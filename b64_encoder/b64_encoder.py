import fileinput

# s_std_in = ''
# for line in fileinput.input():
#     s_std_in+=line
#     continue
# test string
s_std_in = 'Hey'
s_std_in = 'He'
s_std_in = 'Heoo'
s_std_in = '🐻🌻 Animals'
s_std_in = '🐻'

bits_string = ''

for character in s_std_in: 
    
    n_bytes_for_char = character.encode(mode='rb')
    print((n_bytes_for_char))

    n_decimal_utf_char = ord(character)
    n_binary_utf_char = bin(n_decimal_utf_char)
    s_binary = str(n_binary_utf_char).replace('b', '')
        
    # if((len(s_binary) % 8) != 0):
    #     n_missing_bits = 8  - (len(s_binary) % 8) 
    #     n_len_to_reach = (len(s_binary) + n_missing_bits)
        
    #     while(len(s_binary) < n_len_to_reach):
    #         # s_binary = '0' + s_binary
    #         s_binary = s_binary + '0'
    
    print('s_binary')
    print(s_binary)

    bits_string+= s_binary

print('bits_string')
print(bits_string)

a_groups_of_six_bits = []
s_group_of_six_bits = ''
for (key, value) in enumerate(bits_string):
    
    s_group_of_six_bits += str(value)

    if((key+1) % 6 == 0): 
        
        a_groups_of_six_bits.append(s_group_of_six_bits)

        s_group_of_six_bits = ''
        
        # print(f'key {key} value {value}')

# append last string to array as well 
if(len(s_group_of_six_bits)>0):
    a_groups_of_six_bits.append(s_group_of_six_bits)

a_decimal_nums_for_b64 = []
a_characters_for_b64 = []

a_b64_characters_table = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/']

print('a_groups_of_six_bits')
print(a_groups_of_six_bits)

for s_group_of_six_bits in a_groups_of_six_bits: 

    while(len(s_group_of_six_bits) < 6): 
        s_group_of_six_bits = s_group_of_six_bits + '0'

    print('s_group_of_six_bits')
    print(s_group_of_six_bits)
    
    n_decimal_for_group_of_six_bits = int(str(s_group_of_six_bits), 2)
    s_b64_character = a_b64_characters_table[n_decimal_for_group_of_six_bits]
    a_decimal_nums_for_b64.append(n_decimal_for_group_of_six_bits)
    a_characters_for_b64.append(s_b64_character)

    
print(s_group_of_six_bits)


# add padding 
n_of_padding_to_add = 4 - (len(a_characters_for_b64) % 4)
a_s_padding = ['='] * n_of_padding_to_add
print('b64 encoded')
print(
    ''.join(a_characters_for_b64)
    +
    ''.join(a_s_padding)
    ) 


# print(bits_string)
# print(s_std_in)
