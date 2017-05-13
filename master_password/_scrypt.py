__all__ = ('scrypt',)

scrypt = None

try:
    scrypt = hashlib.scrypt
except AttributeError:
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
    raise error(msg)
