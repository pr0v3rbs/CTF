# Reverse4bit.py

import sys

if len(sys.argv) != 2 :
    print 'Usage : python Reverse4bit.py <input file>'
    exit()

f = open(sys.argv[1], "rb")
data = f.read()
f.close()

result = ''
for i in data :
    num = ord(i)
    result = chr(((num & 0xf0) >> 4) + ((num & 0x0f) << 4)) + result

print result
