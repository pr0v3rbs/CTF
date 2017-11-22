# ReverseByte.py

import sys

if len(sys.argv) != 3 :
    print 'Usage : python ReverseByte.py <input file> <output file>'
    exit()

f = open(sys.argv[1], "rb")
data = f.read()
data = data[::-1]
f.close()

f = open(sys.argv[2], "wb")
f.write(data)
f.close()
