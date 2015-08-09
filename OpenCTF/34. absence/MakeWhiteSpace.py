# MakeWhiteSpace.py

import sys

if len(sys.argv) != 2 :
    print 'Usage : python MakeWhiteSpace.py <input file>'
    exit()

f = open(sys.argv[1], 'r')
data = f.read()
f.close()

result = ''
for i in data :
	if ord(i) == 0x20 or ord(i) == 0x09 or ord(i) == 0x0A :
		if ord(i) == 0x20 :
			result += 'S'
		if ord(i) == 0x09 :
			result += 'T'
		if ord(i) == 0x0A :
			result += 'L'
		result += i
print result
