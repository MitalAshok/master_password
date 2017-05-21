__all__ = ('scrypt',)

scrypt = None

try:
    from hashlib import scrypt
except ImportError:
    try:
        from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
        from cryptography.hazmat.backends import default_backend
        backend = default_backend()
        def scrypt(password, salt, N, r, p, dk_len):
            kdf = Scrypt(salt, dk_len, N, r, p, backend)
            return kdf.derive(password)
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
