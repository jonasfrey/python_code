from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable


from fontTools.ttLib import TTFont

font = TTFont('/home/jf18j492/code/python_code/NotoColorEmoji.ttf')

cmap = font['cmap']
t = cmap.getBestCmap()
s = font.getGlyphSet()

def width(c):
    if ord(c) in t and t[ord(c)] in s:
        return s[t[ord(c)]].width
    else:
        return s['.notdef'].width

assert width('a') == 512
assert width('弢') == 512
assert width(chr(0x081C)) == 0
assert width(chr(0x11A7)) == 1024

#print(font.__dict__)

# cmap = font['cmap']

# t = cmap.getcmap(3,1).cmap
# s = font.getGlyphSet()
# units_per_em = font['head'].unitsPerEm

# def getTextWidth(text,pointSize):
#     total = 0
#     for c in text:
#         if ord(c) in t and t[ord(c)] in s:
#             total += s[t[ord(c)]].width
#         else:
#             total += s['.notdef'].width
#     total = total*float(pointSize)/units_per_em;
#     return total

# text = 'This is a test'

# width = getTextWidth(text,12)

# print ('Text: "%s"' % text)
# print ('Width in points: %f' % width)
# print ('Width in inches: %f' % (width/72))
# print ('Width in cm: %f' % (width*2.54/72))
# print ('Width in WP Units: %f' % (width*1200/72))