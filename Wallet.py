from utils import *

class Wallet():
    def __init__(self, name: str = "mlem"):
        self.name = name
        random_seed = random.randint(0, 1000)
        self.private_key = hash_unicode(str(random_seed))
        self.private_key_bin = ''.join(format(ord(x), 'b') for x in self.private_key)
        self.private_key_int = int(w.private_key_bin, base=2)

    def __repr__(self):
        return repr('BChain ' + self.name)

    def hash256(self):
        return hash_unicode(repr(self))

if __name__ == "__main__":
    pass
    w = Wallet()
    print(w.private_key)
    print(w.private_key_bin)
    print(int(w.private_key_bin, base=2))
    # print(key)
    # print(type(key))
    # print(type(w.private_key))
    # print(key*w.private_key)
