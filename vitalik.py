code_strings = {
    2: '01',
    10: '0123456789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    58: '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
    256: ''.join([chr(x) for x in range(256)])
}

def get_code_string(base):
    if base not in code_strings:
        raise ValueError("Invalid base!")
    return code_strings[base]

def encode(val, base, minlen=0):
    base, minlen = int(base), int(minlen)
    code_string = get_code_string(base)
    result_bytes = bytes()
    while val > 0:
        curcode = code_string[val % base]
        result_bytes = bytes([ord(curcode)]) + result_bytes
        val //= base

    pad_size = minlen - len(result_bytes)

    padding_element = b'\x00' if base == 256 else b'1' \
        if base == 58 else b'0'
    if (pad_size > 0):
        result_bytes = padding_element*pad_size + result_bytes

    result_string = ''.join([chr(y) for y in result_bytes])
    result = result_bytes if base == 256 else result_string

    return result

def encode_pubkey(pub: Tuple[int, int], formt: str):
    if formt == 'decimal': return pub
    elif formt == 'bin': return b'\x04' + encode(pub[0], 256, 32) + encode(pub[1], 256, 32)
    elif formt == 'hex': return '04' + encode(pub[0], 16, 64) + encode(pub[1], 16, 64)

def from_int_to_byte(a):
        return bytes([a])

def from_string_to_bytes(a):
        return a if isinstance(a, bytes) else bytes(a, 'utf-8')

def bin_dbl_sha256(s):
        bytes_to_hash = from_string_to_bytes(s)
        return hashlib.sha256(hashlib.sha256(bytes_to_hash).digest()).digest()

def lpad(msg, symbol, length):
        if len(msg) >= length:
            return msg
        return symbol * (length - len(msg)) + msg

def decode(string, base):
        if base == 256 and isinstance(string, str):
            string = bytes(bytearray.fromhex(string))
        base = int(base)
        code_string = get_code_string(base)
        result = 0
        if base == 256:
            def extract(d, cs):
                return d
        else:
            def extract(d, cs):
                return cs.find(d if isinstance(d, str) else chr(d))

        if base == 16:
            string = string.lower()
        while len(string) > 0:
            result *= base
            result += extract(string[0], code_string)
            string = string[1:]
        return result


def changebase(string, frm, to, minlen=0):
        if frm == to:
            return lpad(string, get_code_string(frm)[0], minlen)
        return encode(decode(string, frm), to, minlen)


def bin_to_b58check(inp, magicbyte=0):
        if magicbyte == 0:
            inp = from_int_to_byte(0) + inp
        while magicbyte > 0:
            inp = from_int_to_byte(magicbyte % 256) + inp
            magicbyte //= 256

        leadingzbytes = 0
        for x in inp:
            if x != 0:
                break
            leadingzbytes += 1

        checksum = bin_dbl_sha256(inp)[:4]
        return '1' * leadingzbytes + changebase(inp+checksum, 256, 58)

from ripemd import RIPEMD160
import binascii

def bin_hash160(string):
    intermed = hashlib.sha256(string).digest()
    digest = ''
    try:
        digest = hashlib.new('ripemd160', intermed).digest()
    except:
        digest = RIPEMD160(intermed).digest()
    return digest

def pubkey_to_address(pubkey, magicbyte=0):
    if isinstance(pubkey, (list, tuple)):
        pubkey = encode_pubkey(pubkey, 'bin')
    if len(pubkey) in [66, 130]:
        return bin_to_b58check(
            bin_hash160(binascii.unhexlify(pubkey)), magicbyte)
    return bin_to_b58check(bin_hash160(pubkey), magicbyte)

def privkey_to_address(priv, magicbyte=0):
    return pubkey_to_address(public_key(priv), magicbyte)
privtoaddr = privkey_to_address