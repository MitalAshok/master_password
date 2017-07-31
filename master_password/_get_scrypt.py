__all__ = ('scrypt',)

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
            from scrypt import hash

            def scrypt(password, salt, N, r, p, dk_len):
                return hash(password, salt, N, r, p, dk_len)
        except ImportError:
            try:
                from pyscrypt import hash

                def scrypt(password, salt, N, r, p, dk_len):
                    return hash(password, salt, N, r, p, dk_len)
            except ImportError:
                msg = "No module named 'cryptography', 'scrypt' or 'pyscrypt'"
                try:
                    error = ModuleNotFoundError(msg)
                except NameError:
                    error = ImportError(msg)

                def scrypt(password, salt, N, r, p, dk_len):
                    raise error
