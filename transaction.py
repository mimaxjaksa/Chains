from utils import *
from wallet import *

class Transaction:
    def __init__(self, from_w: Wallet, to_w: Wallet, message: str = "mlem", amount: float = 0):
        self.message = message
        self.amount = amount
        self.from_w = from_w
        self.to_w = to_w
        self.processed = False
    
    def process(self):
        self.from_w.take_amount(self.amount)
        # self.to_w.add_amount(self.amount)
        self.to_w.utxo.append(self)
        self.processed = True
    
    def __repr__(self) -> str:
        return f"Transaction: \n\tmessage: {self.message}, \n\tfrom wallet: {self.from_w.name}, \n\tto wallet: {self.to_w.name}, \n\tamount: {self.amount}, \n\tprocessed: {self.processed}"


if __name__ == "__main__":
    w1 = Wallet("Alice", 10)
    w2 = Wallet("Bob", 20)
    print(w1)
    print(w2)

    t = Transaction(w1, w2, amount=3.2)

    print(t)
    t.process()
    print(t)

    print(w1)
    print(w2)
