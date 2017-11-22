import pwnable
import base64
import time
import subprocess

p = pwnable.Pwnable()
p.Connect('bad2.eatpwnnosleep.com', 8888)

def ExtractBin(data):
    if data.find("SCTF{") != -1:
        print data
        exit()
    if data.find("Fail") != -1: exit()
    data = data[data.find('f0VMRg') : data.rfind('Send')]
    return base64.b64decode(data)

def GetFunctionAsm(lines, functionName, asmIdx):
    for idx, line in enumerate(lines):
        if line.find('<' + functionName + '>:') != -1:
            return lines[idx + asmIdx]

def Patch(data, stage):
    if stage == 1:
        print 'stage1'
        lines = subprocess.check_output(['objdump', '-d', 'ori']).split('\n')
        dstInfoLine = GetFunctionAsm(lines, 'get_int', 5)

        idx = int(dstInfoLine[5:8], 16)
        if dstInfoLine[10:12] == '68': # push 4bytes
            return data[:idx+1] + p.p4(0x10) + data[idx+5:]
        else: # '6a' push 1byte
            return data[:idx+1] + chr(0x10) + data[idx+2:]

    elif stage == 2:
        print 'stage2'
        lines = subprocess.check_output(['objdump', '-d', 'ori2']).split('\n')
        dstInfoLine = GetFunctionAsm(lines, 'get_file', 9)
        srcInfoLine = GetFunctionAsm(lines, 'create_file', 18)

        size = int(srcInfoLine[srcInfoLine.rfind('0x')+2:], 16)
        idx = int(dstInfoLine[5:8], 16)
        if dstInfoLine[10:12] == '68': # push 4bytes
            return data[:idx+1] + p.p4(size) + data[idx+5:]
        else: # '6a' push 1byte
            return data[:idx+1] + chr(size) + data[idx+2:]

    elif stage == 3:
        print 'stage3'
        lines = subprocess.check_output(['objdump', '-d', './ori3']).split('\n')
        dstInfoLine = GetFunctionAsm(lines, 'modify_file', 14)
        srcInfoLine = GetFunctionAsm(lines, 'create_file', 18)

        size = int(srcInfoLine[srcInfoLine.rfind('0x')+2:], 16)
        idx = int(dstInfoLine[5:8], 16)
        if dstInfoLine[10:12] == '68': # push 4bytes
            return data[:idx+1] + p.p4(size) + data[idx+5:]
        else: # '6a' push 1byte
            return data[:idx+1] + chr(size) + data[idx+2:]

count = 1
while True:
    data = ExtractBin(p.ReadUntil('change)'))
    open('ori', 'w').write(data)
    newData = Patch(data, 1)
    open('bin', 'w').write(newData)

    if count > 30:
        data = newData
        open('ori2', 'w').write(data)
        newData = Patch(data, 2)
        open('bin2', 'w').write(newData)

    if count > 60:
        data = newData
        open('ori3', 'w').write(data)
        newData = Patch(data, 3)
        open('bin3', 'w').write(newData)

    p.Sendline(base64.b64encode(newData))
    print('[*] round %d' % count)
    count += 1
