#moonwalk
**Category:** forensics, reversing
**Point:** 50
**Description:**

> ?

##Write-up

###Stage1
The data file(moonwalk) is given.

It looked like a zip archive, but I couldn't open.

Compare it(moonwalk) with normal zip archive, I came to know that 'moonwalk' was reversed by 8bit(byte) base.

Repair zip archive with my python code. And I got 'metsys.elif' file.

'''
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
'''

###Stage2
'metsys.elif' file is a reversed 'filesystem' file by 8bit(byte) base, too.

And I was used 'Accessdata FTK imager' forensic tool to analyze 'metsys.elif' filesystem file.

Finally I found 'txt.galf' file, and I reversed it by 4bit base. I got flag.

> # Reverse4bit.py
>
> import sys
>
> if len(sys.argv) != 2 :
>     print 'Usage : python Reverse4bit.py <input file>'
>     exit()
>
> f = open(sys.argv[1], "rb")
> data = f.read()
> f.close()
>
> result = ''
> for i in data :
>     num = ord(i)
>     result = chr(((num & 0xf0) >> 4) + ((num & 0x0f) << 4)) + result
>
> print result

The flag is `_ju57_7urn_Ar0unD_and_w41k_aw4y_`