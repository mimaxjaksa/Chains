from utils import *

class Wallet():
    def __init__(self, name: str = "mlem"):
        self.name = name
        random_seed = random.randint(0, 1000)
        # self.private_key = hash_unicode(str(random_seed))
        self.private_key = 0xA0DC65FFCA799873CBEA0AC274015B9526505DAAAED385155425F7337704883E #find a way how to generate this
        # self.private_key = f"0x{hash_unicode(str(random_seed))}"
        # self.private_key_bin = ''.join(format(ord(x), 'b') for x in self.private_key)
        # self.private_key_int = int(self.private_key_bin, base=2)

    def __repr__(self):
        return repr('BChain ' + self.name)

    def hash256(self):
        return hash_unicode(repr(self))

if __name__ == "__main__":
    pass
    w = Wallet()
    # print(w.private_key)
    pub_k = ecc_multiply(G, w.private_key)
    # print(G*w.private_key_int)