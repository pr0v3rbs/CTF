import string
import md5

alpha = string.ascii_uppercase

m = alpha + '{}'
l = []
for i in range(len(m)):
	l.append(m)
	m = m[1:] + m[0]

charMap = {}
for i, j in enumerate(m):
	charMap[j] = i

cipher = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ"
key = 'VIGENERE'

for i1 in m:
	for i2 in m:
		for i3 in m:
			for i4 in m:
				temKey = key + i1 + i2 + i3 + i4
				decodeStr = ''
				keyIdx = 0
				for i in cipher:
					for j in l:
						if j[charMap[temKey[keyIdx]]] == i:
							decodeStr += j[0]
							break
					keyIdx = (keyIdx + 1) % len(temKey)
				if md5.new(decodeStr).digest() == '\xf5\x28\xa6\xab\x91\x4c\x1e\xcf\x85\x6a\x1d\x93\x10\x39\x48\xfe':
					print '[*] find!!'
					print decodeStr
					exit()

print '[*] decode fail!!'
