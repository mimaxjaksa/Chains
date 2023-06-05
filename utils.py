"""
Some sources: 

- https://github.com/wobine/blackboard101/blob/master/EllipticCurvesPart4-PrivateKeyToPublicKey.py
- https://wiki.openssl.org/index.php/Elliptic_Curve_Cryptography
- https://onyb.gitbook.io/secp256k1-python/point-addition-in-python

"""
# import hashlib
# import random

from dataclasses import dataclass

# # The proven prime
# p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1

# # Number of points in the field, defined by N*G = I
# # TODO: Why is this different from p?
# N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# # These two define the elliptic curve. y^2 = x^3 + A * x + B
# A = 0
# B = 7

# # This is our generator point. Trillions of dif ones possible
# # For prime order curves, every point in a generator point
# Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
# Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
# G = (Gx, Gy)


@dataclass
class PrimeGaloisField:
    prime: int

    def __contains__(self, field_value: "FieldElement") -> bool:
        # called whenever you do: <FieldElement> in <PrimeGaloisField>
        return 0 <= field_value.value < self.prime
    
@dataclass
class FieldElement:
    value: int
    field: PrimeGaloisField

    def __repr__(self):
        return "0x" + f"{self.value:x}".zfill(64)
        
    @property
    def P(self) -> int:
        return self.field.prime
    
    def __add__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value + other.value) % self.P,
            field=self.field
        )
    
    def __sub__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value - other.value) % self.P,
            field=self.field
        )

    def __rmul__(self, scalar: int) -> "FieldValue":
        return FieldElement(
            value=(self.value * scalar) % self.P,
            field=self.field
        )

    def __mul__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value * other.value) % self.P,
            field=self.field
        )
        
    def __pow__(self, exponent: int) -> "FieldElement":
        return FieldElement(
            value=pow(self.value, exponent, self.P),
            field=self.field
        )

    def __truediv__(self, other: "FieldElement") -> "FieldElement":
        other_inv = other ** -1
        return self * other_inv


@dataclass
class EllipticCurve:
    a: int
    b: int

    field: PrimeGaloisField
    
    def __contains__(self, point: "Point") -> bool:
        x, y = point.x, point.y
        return y ** 2 == x ** 3 + self.a * x + self.b

    def __post_init__(self):
        # Encapsulate int parameters in FieldElement
        self.a = FieldElement(self.a, self.field)
        self.b = FieldElement(self.b, self.field)
    
        # Check for membership of curve parameters in the field.
        if self.a not in self.field or self.b not in self.field:
            raise ValueError

P: int = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)
field = PrimeGaloisField(prime=P)

# Elliptic curve parameters A and B of the curve : y² = x³ Ax + B
A: int = 0
B: int = 7

secp256k1 = EllipticCurve(
    a=A,
    b=B,
    field=field
)


inf = float("inf")

@dataclass
class Point:
    x: int
    y: int

    curve: EllipticCurve

    def __post_init__(self):
        # Ignore validation for I
        if self.x is None and self.y is None:
            return

        # Encapsulate int coordinates in FieldElement
        self.x = FieldElement(self.x, self.curve.field)
        self.y = FieldElement(self.y, self.curve.field)

        # Verify if the point satisfies the curve equation
        if self not in self.curve:
            raise ValueError

    def __add__(self, other):
        if self == I:
            return other

        if other == I:
            return self

        if self.x == other.x and self.y == (-1 * other.y):
            return I

        if self.x != other.x:
            x1, x2 = self.x, other.x
            y1, y2 = self.y, other.y

            s = (y2 - y1) / (x2 - x1)
            x3 = s ** 2 - x1 - x2
            y3 = s * (x1 - x3) - y1

            return self.__class__(
                x=x3.value,
                y=y3.value,
                curve=secp256k1
            )

        if self == other and self.y == inf:
            return I

        if self == other:
            x1, y1, a = self.x, self.y, self.curve.a

            s = (3 * x1 ** 2 + a) / (2 * y1)
            x3 = s ** 2 - 2 * x1
            y3 = s * (x1 - x3) - y1

            return self.__class__(
                x=x3.value,
                y=y3.value,
                curve=secp256k1
            )
    
    def __rmul__(self, scalar: int) -> "Point":
        current = self
        result = I
        while scalar:
            if scalar & 1:  # same as scalar % 2
                result = result + current
            current = current + current  # point doubling
            scalar >>= 1  # same as scalar / 2
        return result


G = Point(
    x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    curve=secp256k1
)

# Order of the group generated by G, such that nG = I
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

I = Point(x=None, y=None, curve=secp256k1)


# def ecc_multiply(gen_point, scalar):
#     if scalar == 0 or scalar >= N:
#         raise Exception("Invalid Scalar/Private Key")
#     scalar_bin = str(bin(scalar))[2:]
#     Q = gen_point
#     for t in reversed(scalar_bin):
#         pass
#     # for i in range(1, len(scalar_bin)):
#     #     Q = double_point(Q)
#     #     if scalar_bin[i] == "1":
#     #         Q = add_points(Q, gen_point)
#     return result

# def double_point(a):
#     Lam = ((3*a[0]*a[0]+A) * modinv((2*a[1]), p)) % p
#     x = (Lam*Lam-2*a[0]) % p
#     y = (Lam*(a[0]-x)-a[1]) % p
#     return (x,y)

# def modinv(a, n = p):
#     lm, hm = 1, 0
#     low, high = a % n, n
#     while low > 1:
#         ratio = high / low
#         nm, new = hm - lm * ratio, high - low * ratio
#         lm, low, hm, high = nm, new, lm, low
#     return lm % n

# def add_points(a, b):
#     LamAdd = ((b[1] - a[1]) * modinv(b[0] - a[0], p)) % p
#     x = (LamAdd * LamAdd - a[0] - b[0]) % p
#     y = (LamAdd * (a[0] - x) - a[1]) % p
#     return (x,y)

# def hash_unicode(a_string):
#     return hashlib.sha256(a_string.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    k = 0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD
    print(G.x.value)
    print(G.y.value)

    a = k*G

    print(a.x)
    print(a.y)
    