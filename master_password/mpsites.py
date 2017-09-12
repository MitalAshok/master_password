# Based on https://github.com/Lyndir/MasterPassword/issues/164#issuecomment-310868274
# See https://github.com/Lyndir/MasterPassword/issues/164

# Unfinished
raise ImportError('Cannot import name \'mpsites\'')

import json
import collections
import base64

from cryptography.hazmat.primitives.ciphers.algorithms import AES


try:
    from master_password._get_scrypt import backend
except ImportError:
    from cryptography.hazmat.backends import default_backend
    backend = default_backend()

from master_password import (
    SCRYPT_N, SCRYPT_r, SCRYPT_p, SCRYPT_dk_len, scrypt, encode_if
)


ENC_ALG = 'A256GCM'
KEY_MGMT_ALG = 'dir'  # TODO: Verify this

_versions = {}


def _version(n):
    def register(f):
        _versions[n] = f
        return f
    return register


def encode(users, default, version=1):
    f = _versions.get(version, None)
    if f is None:
        raise ValueError('Invalid version: {!r}'.format(version))
    return f(users, default)


@_version(1)
@_version(1.0)
def _encode(users, default):
    users_dict = {}
    mpsites = {
        'version': 2,
        'default': getattr(default, 'full_name', default),
        'users': users_dict
    }
    for user in users:
        if not isinstance(user, User):
            users_dict[user[0]] = user[1]
            continue
        user_dict = {}
        users_dict[user.full_name] = user_dict

        keyhash = jwcrypto.common.base64url_encode(
            scrypt(encode_if(user.key), encode_if(user.key),
                   SCRYPT_N, SCRYPT_r, SCRYPT_p, SCRYPT_dk_len)
        )
        keyhash_version = 'v' + str(user.version)
        user_dict['keyhash'] = keyhash
        user_dict['keyhash_version'] = keyhash_version

        plaintext = jwcrypto.common.json_encode(user.sites)
        # TODO: salt and info.
        kdf = HKDF(
            hashes.SHA256(), 64, salt=b'???', info=b'???', backend=backend
        )
        cipher = jwcrypto.jwe.JWE(plaintext=plaintext, protected={
            'alg': KEY_MGMT_ALG,
            'enc': ENC_ALG,
            'keyhash': keyhash,
            'keyhash_version': keyhash_version
        }, algs=[ENC_ALG], recipient=kdf.derive(user.key))

        user_dict['sites'] = cipher.serialize()
    return json.dumps(mpsites)

User = collections.namedtuple('User', ('key', 'full_name', 'sites', 'version'))

# raise NotImplementedError
