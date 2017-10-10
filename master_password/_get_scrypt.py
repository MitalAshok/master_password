__all__ = ('scrypt',)

try:
    from hashlib import scrypt as hash

    _IMPLEMENTATION = 'hashlib'

    def scrypt(password, salt, N, r, p, dk_len):
        return hash(password, salt=salt, n=N, r=r, p=p, dklen=dk_len, maxmem=(128 * r * (N + p + 2)))
except ImportError:
    try:
        from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
        from cryptography.hazmat.backends import default_backend
        backend = default_backend()

        _IMPLEMENTATION = 'cryptography'

        def scrypt(password, salt, N, r, p, dk_len):
            kdf = Scrypt(salt, dk_len, N, r, p, backend)
            return kdf.derive(password)
    except ImportError:
        try:
            from scrypt import hash

            _IMPLEMENTATION = 'scrypt'

            def scrypt(password, salt, N, r, p, dk_len):
                return hash(password, salt, N, r, p, dk_len)
        except ImportError:
            try:
                from pyscrypt import hash

                _IMPLEMENTATION = 'pyscrypt'

                def scrypt(password, salt, N, r, p, dk_len):
                    return hash(password, salt, N, r, p, dk_len)
            except ImportError:
                _IMPLEMENTATION = None

                msg = "No module named 'cryptography', 'scrypt' or 'pyscrypt'"
                try:
                    error = ModuleNotFoundError(msg)
                except NameError:
                    error = ImportError(msg)

                def scrypt(password, salt, N, r, p, dk_len):
                    raise error
