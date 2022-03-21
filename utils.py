import hashlib
import random
from Crypto.PublicKey import ECC

key = ECC.generate(curve='P-256') #TODO Is this the exact curve used?

def hash_unicode(a_string):
    return hashlib.sha256(a_string.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    pass
