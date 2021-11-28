# -*- coding: utf-8 -*-
# for usage of non ascii characters , 
# we need to define the encoding with
# the first line !

import sys

if sys.version_info >= (3, 0):
    sys.stdout.write("Sorry, requires Python 2.x, not Python 3.x\n")
    sys.exit(1)

# credits https://www.youtube.com/watch?v=ut74oHojxqo 


# when we define a normal string
s_emoji = "👍"
# the len function will return 
# the length of the bytes used for this string
# which is 4
print(len(s_emoji))

# if we try to access the indexes of the string 
print(s_emoji[0])
print(s_emoji[1])
print(s_emoji[2])
print(s_emoji[3])
# we will get the single bytes the string consists of 

print('now with using unicode aware strings')

# to define a string unicode aware we have to prefix it with 'u'
s_emoji_unicode_aware = u"👍"

print(len(s_emoji_unicode_aware))

print(s_emoji_unicode_aware[0])
# accessing a higher index  wont work since the string length is only 1
# print(s_emoji_unicode_aware[1]) # this wont work


# ! run this example with python 2 (python name_of_the_script.py) !

# character modifiers 

s_emoji_modified = '👍🟫'
print(len(s_emoji_modified))


s_emoji_modified_unicode_aware = u'👍🟫'
print(len(s_emoji_modified_unicode_aware))

