# Based on https://gist.github.com/sscherfke/fe58bb5bcc3e5028b9199902bf895d7e
# See https://github.com/Lyndir/MasterPassword/issues/164

import base64
import json
import collections

import jwcrypto.jwe

from master_password import (
    SCRYPT_N, SCRYPT_r, SCRYPT_p, SCRYPT_dk_len, scrypt, encode_if
)


def encode(users, default, version=2):
    if version == 2:
        return _encode_v2(users, default)
    raise ValueError('Invalid version: {!r}'.format(version))


def _encode_v2(users, default):
    users_dict = {}
    mpsites = {
        'version': 2,
        'default': getattr(getattr(default, 'mpw', default), 'full_name', default),
        'users': users_dict
    }
    for user in users:
        user_dict = {}
        users_dict[user.mpw.full_name] = user_dict

        keyhash = scrypt(encode_if(user.mpw.key), encode_if(user.mpw.key),
                         SCRYPT_N, SCRYPT_r, SCRYPT_p, SCRYPT_dk_len)
        users_dict['keyhash'] = base64.urlsafe_b64encode(keyhash)
        users_dict['keyhash_version'] = 'v' + str(user.mpw.version)

        sites = {}
        user_dict['sites'] = sites

        # TODO: figure this out

        sites['ciphertext'] = "<JWE AES256-GCM encrypted sites>"
        sites['iv'] = "<JWE initialization header>"
        sites['protected'] = "<JWE protected header>",
        sites['tag'] = "<JWE tag>"

    return json.dumps(mpsites)


class User(object):
    __metaclass__ = collections.namedtuple('User', ('mpw', 'sites'))

    __slots__ = ()


raise NotImplementedError
