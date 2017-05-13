__all__ = ('scrypt',)

scrypt = None

try:
    from hashlib import scrypt
except ImportError:
    try:
        from scrypt import hash as scrypt
    except ImportError:
        try:
            from pyscrypt import hash as scrypt
        except ImportError:
            pass

if scrypt is None:
    msg = "No module named 'scrypt' or 'pyscrypt'"
    try:
        error = ModuleNotFoundError
    except NameError:
        error = ImportError
    def scrypt(N, r, p, dk_len):
        raise error(msg)
