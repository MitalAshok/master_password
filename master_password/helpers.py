__all__ = ('encode_if', 'decode_if', 'uint8_list')

unicode = type(u'')


def encode_if(s, errors='strict', encoding='utf-8'):
    if isinstance(s, unicode):
        return unicode.encode(s, encoding, errors)
    # No need to account for long, as it will just overflow
    if isinstance(s, int):
        raise TypeError('Cannot interpret "{}" object as bytes.'.format(type(s)))
    return bytes(s)


def decode_if(s, errors='strict', encoding='utf-8'):
    if isinstance(s, bytes):
        return bytes.decode(s, encoding, errors)
    if isinstance(s, bytearray):
        return bytearray.decode(s, encoding, errors)
    if isinstance(s, (tuple, list)):
        return bytearray(s).decode(encoding, errors)
    return unicode(s)


if hasattr(int, 'to_bytes'):
    def uint8_list(uint_32):
        return (uint_32 & 0xffffffff).to_bytes(4, 'big')
else:
    def uint8_list(uint_32):
        return bytearray([
            (uint_32 >> 0o30) & 0xff,
            (uint_32 >> 0o20) & 0xff,
            (uint_32 >> 0o10) & 0xff,
            (uint_32 >> 0o00) & 0xff
        ])
