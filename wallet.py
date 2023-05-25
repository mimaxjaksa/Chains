from utils import *

class Wallet():
    def __init__(self, name: str = "mlem", amount: float = 0):
        self.name = name
        self.amount = amount
        self.utxo = []
        
        
        # random_seed = random.randint(0, 1000)
        # self.private_key = hash_unicode(str(random_seed))
        # self.private_key = 0xA0DC65FFCA799873CBEA0AC274015B9526505DAAAED385155425F7337704883E #find a way how to generate this
        # self.private_key = f"0x{hash_unicode(str(random_seed))}"
        # self.private_key_bin = ''.join(format(ord(x), 'b') for x in self.private_key)
        # self.private_key_int = int(self.private_key_bin, base=2)

    def take_amount(self, amount):
        self.amount -= amount

    def add_amount(self, amount):
        self.amount += amount

    def get_amount(self) -> float:
        return self.amount + sum(utxo_.amount for utxo_ in self.utxo)

    def __repr__(self) -> str:
        return f"Wallet: \n\tname: {self.name}, \n\tamount: {self.get_amount()}"

    def hash256(self) -> str:
        return hash_unicode(repr(self))

if __name__ == "__main__":
    w1 = Wallet("Alice", 10)
    w2 = Wallet("Bob", 20)
    print(w1)
    print(w2)