from utils import *

class Block():
    pass

class BlockChain():
    def __init__(self, name: str = "mlem"):
        self.name = name
        self.block_list = []


    def __repr__(self):
        return repr('BChain ' + self.name)

if __name__ == "__main__":
    pass