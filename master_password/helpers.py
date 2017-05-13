__all__ = ('encode_if', 'decode_if', 'uint8_list')


def encode_if(s, errors='strict', encoding='utf-8'):
    if isinstance(s, str):
        return str.encode(s, encoding, errors)
    return bytes(s)


def decode_if(s, errors='strict', encoding='utf-8'):
    if isinstance(s, (tuple, list)):
        return bytearray(s).decode(encoding, errors)
    if isinstance(s, (bytes, bytearray)):
        return s.decode(encoding, errors)
    return str(s)


def uint8_list(uint_32):
    return bytearray([
        (uint_32 >> 0o30) & 0xff,
        (uint_32 >> 0o20) & 0xff,
        (uint_32 >> 0o10) & 0xff,
        (uint_32 >> 0o00) & 0xff])
