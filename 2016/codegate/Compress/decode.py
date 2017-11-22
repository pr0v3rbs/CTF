import md5

def encode(input_string):
    h = md5.md5(input_string[:4]).hexdigest()
    table = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': 8,
        'i': 9,
        'j': 0
    }
    out = ""
    prev = ""
    stage1 = []
    stage2 = []
    stage3 = ""
    passbyte = -1
    for ch in input_string:
        if ch in table.keys():
            stage1.append(table[ch])
        else:
            stage1.append(ch)

    for index, ch in enumerate(stage1):
        if len(stage1) <= index+1:
            if index != passbyte:
                stage2.append(ch)
            break

        if passbyte != -1 and passbyte == index:
            continue

        if type(ch) == int and type(stage1[index+1])==int:
            tmp = ch << 4
            tmp |= stage1[index+1]
            stage2.append(tmp)
            passbyte = index+1
        else:
            stage2.append(ch)

    for ch in stage2:
        if type(ch) == int:
            stage3 += chr(ch)
        else:
            stage3 += ch

    for index, ch in enumerate(stage3):
        if index >= len(h):
            choice = 0
        else:
            choice = index

        out += chr(ord(ch) ^ ord(h[choice]))

    return out

encoded = "~u/\x15mK\x11N`[^\x13E2JKj0K;3^D3\x18\x15g\xbc\\Gb\x14T\x19E"

s='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

md5List = []
for i1 in s:
    for i2 in s:
        for i3 in s:
            for i4 in s:
                out = encode(i1+i2+i3+i4)
                if ((len(out) == 2 and encoded[0] == out[0] and encoded[1] == out[1]) or
                    (len(out) == 3 and encoded[0] == out[0] and encoded[1] == out[1] and encoded[2] == out[2]) or
                    (len(out) == 4 and encoded[0] == out[0] and encoded[1] == out[1] and encoded[2] == out[2] and encoded[3] == out[3])):
                    print i1+i2+i3+i4
                    md5List.append(md5.md5(i1+i2+i3+i4).hexdigest())

print md5List

reverseTable = {
    1:'a',
    2:'b',
    3:'c',
    4:'d',
    5:'e',
    6:'f',
    7:'g',
    8:'h',
    9:'i',
    0:'j'
}

for md5Value in md5List:
    decoded=''
    result=''

    for index, ch in enumerate(encoded):
        if index >= len(md5Value):
            choice = 0
        else:
            choice = index
        decoded += chr(ord(ch) ^ ord(md5Value[choice]))
    print repr(decoded)

    for ch in decoded:
        if 0x20 <= ord(ch) < 128:
            result += ch
            continue
        for i in [0,1,2,3,4,5,6,7,8,9]:
            for j in [0,1,2,3,4,5,6,7,8,9]:
                tem = (i << 4)|j
                if (tem == ord(ch)):
                    if i != 0:
                        result += reverseTable[i]
                    result += reverseTable[j]

    print result + "\n"
