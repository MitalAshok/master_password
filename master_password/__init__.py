#!/usr/bin/env python

"""
OOP implementation of the Master Password algorithm

USAGE:

>>> mpw = MPW('Your Full Name', 'Your secret password')
>>> mpw.password('example.org')
"Yoha4'DofsDevo"
>>> mpw.login('example.org')
"joqhutixe"
>>> mpw.answer('example.org')
"sifl pir mejfapo bas"
>>> mpw.answer('example.org', counter=1, context='What was your first pet?')
"ni fabna kaf luregwi"
"""

import hmac
import hashlib

import master_password.helpers as helpers
import master_password.datatypes as datatypes

from master_password.helpers import encode_if, decode_if, uint8_list
from master_password.datatypes import MPWNameSpace, MPWTemplate

from master_password._get_scrypt import scrypt


__author__ = 'Mital Ashok'
__credits__ = ['Maarten Billemont',  # Creator of the Master Password algorithm
               'Mital Ashok']
__license__ = 'GPL-3.0'
__version__ = '1.3.0'
__maintainer__ = 'Mital Ashok'
__author_email__ = __email__ = 'mital.vaja@googlemail.com'
__status__ = 'Production'

__all__ = ('MPWNameSpace', 'MPWTemplate', 'MPW_DEFAULT_NAMESPACE', 'MPW')

MPW_DEFAULT_NAMESPACE = datatypes.default

SCRYPT_N = 32768
SCRYPT_r = 8
SCRYPT_p = 2
SCRYPT_dk_len = 64


class MPW(tuple):
    """Represents information to do the Master Password algorithm"""

    def __new__(
            cls, full_name, master_password, namespace=MPW_DEFAULT_NAMESPACE,
            version=3, keep_name=True
    ):
        """
        Create a new MPW object by calculating the key from
        the full_name and master_password

        full_name: The full full_name of the person to calculate the key with
        master_password: The password to calculate the key with
        namespace: The namespace to caculate the key with and default namespaces
          for helper methods
        version: The version of master password to use (0 to 3)
        keep_name: Whether or not to store the full_name in the class
        """
        salt = MPW.calculate_salt(encode_if(full_name), namespace)
        key = MPW.calculate_key(master_password, salt)
        del master_password
        if not keep_name:
            full_name = None
        else:
            full_name = decode_if(full_name)
        return super(MPW, cls).__new__(cls, (key, namespace, version, full_name))

    def __init__(
            self, full_name, master_password, namespace=None,
            version=None, keep_name=None
    ):
        super(MPW, self).__init__()

    @classmethod
    def from_key(cls, key, full_name=None, namespace=MPW_DEFAULT_NAMESPACE,
                 version=3):
        """Create a new MPW from a pre-calculated key"""
        if full_name is not None:
            full_name = decode_if(full_name)
        return super(MPW, cls).__new__(
            cls, (encode_if(key), namespace, version, full_name)
        )

    @staticmethod
    def calculate_salt(full_name, namespace=MPW_DEFAULT_NAMESPACE):
        salt = bytearray(encode_if(getattr(namespace, 'name', namespace)))
        salt.extend(uint8_list(len(full_name)))
        salt.extend(encode_if(full_name))
        return bytes(salt)

    @staticmethod
    def calculate_key(master_password, salt):
        return bytearray(scrypt(
            encode_if(master_password), salt,
            SCRYPT_N, SCRYPT_r, SCRYPT_p, SCRYPT_dk_len
        ))

    def seed(self, site, namespace=None, counter=1, context=None):
        if namespace is None:
            namespace = self.namespace.name
        site = encode_if(site)
        data = bytearray(encode_if(getattr(namespace, 'name', namespace)))
        data.extend(uint8_list(len(site)))
        data.extend(site)
        data.extend(uint8_list(counter))

        if context:  # is not None:
            context = encode_if(context)
            data.extend(uint8_list(len(context)))
            data.extend(context)

        return bytearray(
            hmac.new(self.key, bytes(data), hashlib.sha256).digest()
        )

    def generate(self, site, counter=1, context=None,
                 template='long', namespace=None, extended=False):
        """
        Generate a password using the MasterPassword algorithm
        
        extended: When True, extends the algorithm in a non-standard way,
        generating a password that is 32 characters long, where the first
        characters equal the password generated with extended = False.
        """
        if namespace is None:
            namespace = self.namespace.name
        else:
            try:
                namespace = getattr(
                    self.namespace, decode_if(namespace), decode_if(namespace)
                )
            except TypeError:
                pass
            except ValueError:
                pass
            namespace = encode_if(getattr(namespace, 'name', namespace))
        seed = self.seed(site, namespace, counter, context)
        if self.version == 0:
            seed = [(0xff if c > 127 else 0) | (c << 8)
                    for i, c in enumerate(seed)]
        template = MPWTemplate.get(template)
        template = template[seed[0] % len(template)]
        chars = MPWTemplate.chars
        password = []
        if extended:
            # This is the only non-standard portion. Slicing it to the correct
            # length makes it compatible.
            i = -1
            for i, s in enumerate(seed[1:]):
                chrs = chars[template[i % len(template)]]
                password.append(chrs[s % len(chrs)])
            chrs = chars[template[(i + 1) % len(template)]]
            password.append(chrs[seed[0] % len(chrs)])
        else:
            for i, c in enumerate(template, 1):
                chrs = chars[c]
                password.append(chrs[seed[i] % len(chrs)])
        return ''.join(password)

    def password(self, site, counter=1, template='long'):
        return self.generate(
            site, counter, None, template, self.namespace.password
        )

    def login(self, site, counter=1):
        return self.generate(site, counter, None, 'name', self.namespace.login)

    def answer(self, site, counter=1, context=''):
        return self.generate(
            site, counter, context, 'phrase', self.namespace.answer
        )

    def pin(self, site, counter=1):
        return self.generate(
            site, counter, None, 'pin', self.namespace.password
        )

    @property
    def key(self):
        return tuple.__getitem__(self, 0)

    @property
    def namespace(self):
        return tuple.__getitem__(self, 1)

    @property
    def version(self):
        return tuple.__getitem__(self, 2)

    @property
    def full_name(self):
        return tuple.__getitem__(self, 3)

    identicon_characters = (
        (   # left_arm
            u'\u2554', u'\u255A', u'\u2570', u'\u2550'
        ),
        (   # body
            u'\u2588', u'\u2591', u'\u2592',
            u'\u2593', u'\u263A', u'\u263B'
        ),
        (   # right_arm
            u'\u2557', u'\u255D', u'\u256F', u'\u2550'
        ),
        (   # accessory
            u'\u25C8', u'\u25CE', u'\u25D0', u'\u25D1', u'\u25D2', u'\u25D3',
            u'\u2600', u'\u2601', u'\u2602', u'\u2603', u'\u2604', u'\u2605',
            u'\u2606', u'\u260E', u'\u260F', u'\u2388', u'\u2302', u'\u2618',
            u'\u2622', u'\u2623', u'\u2615', u'\u231A', u'\u231B', u'\u23F0',
            u'\u26A1', u'\u26C4', u'\u26C5', u'\u2614', u'\u2654', u'\u2655',
            u'\u2656', u'\u2657', u'\u2658', u'\u2659', u'\u265A', u'\u265B',
            u'\u265C', u'\u265D', u'\u265E', u'\u265F', u'\u2668', u'\u2669',
            u'\u266A', u'\u266B', u'\u2690', u'\u2691', u'\u2694', u'\u2696',
            u'\u2699', u'\u26A0', u'\u2318', u'\u23CE', u'\u2704', u'\u2706',
            u'\u2708', u'\u2709', u'\u270C'
        )
    )

    @classmethod
    def identicon(cls, full_name, master_password):
        seed = bytearray(hmac.new(
            encode_if(master_password), encode_if(full_name), hashlib.sha256
        ).digest())
        return ''.join(
            c[seed[i] % len(c)] for i, c in enumerate(cls.identicon_characters)
        )

    def __repr__(self):
        if self.full_name is None:
            info = 'for <anonymous> at'
        else:
            info = 'for {!r} at'.format(self.full_name)
        repr_ = info.join(object.__repr__(self).rsplit('at', 1))
        if self.namespace.name is not None:
            return '{} with namespace {!r}>'.format(
                repr_[:-1], self.namespace.name.decode()
            )
        return repr_

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, MPW):
            if (
                self.key == other.key and
                self.namespace == other.namespace and
                self.version == other.version
            ):
                if self.full_name is None or other.full_name is None:
                    return True
                if self.full_name == other.full_name:
                    return True
            return False
        return NotImplemented

    def __ne__(self, other):
        eq = self.__eq__(other)
        if eq is NotImplemented:
            return NotImplemented
        return not eq

    def __ge__(self, other):
        return NotImplemented

    def __gt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __lt__(self, other):
        return NotImplemented

    __add__ = None
    __contains__ = None
    __getitem__ = None
    __iter__ = None
    __len__ = None
    __mul__ = None
    __rmul__ = None
    count = None
    index = None


if __name__ == '__main__':
    import sys
    from master_password.__main__ import main
    main(sys.argv[1:])
