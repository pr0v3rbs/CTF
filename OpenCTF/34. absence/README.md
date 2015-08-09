#absence
**Category:** scripting, misc
**Point:** 200
**Description:**

> What you see is what you get

##Write-up

c source code is given.

First I complied the source code and excuted. It printed `f1@g[This is not the code you'r`, but it was not the flag.

I looked closely at the source code. I found that 'for loop' didn't print all decrypted string. I fixed it(32->33), and the program did print 'e'. But I still did not find the real flag.

I looked closely at the source code harder!. And I found that source code have many 'tab', 'space', 'line feed' more than normal.

I makde the whitespace source code from c source code. And excuted on 'http://www.tutorialspoint.com/execute_whitespace_online.php'.

```python
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
```

Finally I got the rest of flag ` lo0kin-fo]`. I got the real flag by concatenated two string. `f1@g[This is not the code you're lo0kin-fo]`

The flag is `This is not the code you're lo0kin-fo`