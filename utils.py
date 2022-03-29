#Most of the code from https://github.com/wobine/blackboard101/blob/master/EllipticCurvesPart4-PrivateKeyToPublicKey.py

import hashlib
import random

p_curve = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1 # The proven prime
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 # Number of points in the field
Acurve = 0; Bcurve = 7 # These two defines the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy) # This is our generator point. Trillions of dif ones possible

def ecc_multiply(gen_point, scalar_hex):
    if scalar_hex == 0 or scalar_hex >= N:
        raise Exception("Invalid Scalar/Private Key")
    scalar_bin = str(bin(scalar_hex))[2:]
    Q = gen_point
    for i in range (1, len(scalar_bin)):
        Q = ECdouble(Q)
        if scalar_bin[i] == "1":
            Q=ECadd(Q, gen_point)
    return (Q)

def ECdouble(a):
    Lam = ((3*a[0]*a[0]+Acurve) * modinv((2*a[1]), p_curve)) % p_curve
    x = (Lam*Lam-2*a[0]) % p_curve
    y = (Lam*(a[0]-x)-a[1]) % p_curve
    return (x,y)

def modinv(a, n = p_curve):
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        ratio = high / low
        nm, new = hm - lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def ECadd(a,b):
    LamAdd = ((b[1] - a[1]) * modinv(b[0] - a[0], p_curve)) % p_curve
    x = (LamAdd * LamAdd - a[0] - b[0]) % p_curve
    y = (LamAdd * (a[0] - x) - a[1]) % p_curve
    return (x,y)

def hash_unicode(a_string):
    return hashlib.sha256(a_string.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    pass