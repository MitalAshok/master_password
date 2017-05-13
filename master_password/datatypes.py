from master_password.helpers import encode_if, decode_if

__all__ = ('MPWTemplate', 'MPWNameSpace', 'default')

DEFAULT_CHARS = {
  ' ': ' ', 'A': 'AEIOUBCDFGHJKLMNPQRSTVWXYZ', 'C': 'BCDFGHJKLMNPQRSTVWXYZ', 'V': 'AEIOU',
  'a': 'AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz', 'c': 'bcdfghjklmnpqrstvwxyz',
  'n': '0123456789', 'o': "@&%?,=[]_:-+*$#!'^~;()/.", 'v': 'aeiou',
  'x': 'AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz0123456789!@#$%^&*()'
}

DEFAULT_TEMPLATES = {
  'basic': ('aaanaaan', 'aannaaan', 'aaannaaa'),
  'long': (
    'CvcvnoCvcvCvcv', 'CvcvCvcvnoCvcv', 'CvcvCvcvCvcvno', 'CvccnoCvcvCvcv',
    'CvccCvcvnoCvcv', 'CvccCvcvCvcvno', 'CvcvnoCvccCvcv', 'CvcvCvccnoCvcv',
    'CvcvCvccCvcvno', 'CvcvnoCvcvCvcc', 'CvcvCvcvnoCvcc', 'CvcvCvcvCvccno',
    'CvccnoCvccCvcv', 'CvccCvccnoCvcv', 'CvccCvccCvcvno', 'CvcvnoCvccCvcc',
    'CvcvCvccnoCvcc', 'CvcvCvccCvccno', 'CvccnoCvcvCvcc', 'CvccCvcvnoCvcc',
    'CvccCvcvCvccno'),
  'maximum': ('anoxxxxxxxxxxxxxxxxx', 'axxxxxxxxxxxxxxxxxno'),
  'medium': ('CvcnoCvc', 'CvcCvcno'),
  'name': ('cvccvcvcv',),
  'phrase': (
    'cvcc cvc cvccvcv cvc', 'cvc cvccvcvcv cvcv', 'cv cvccv cvc cvcvccv'),
  'pin': ('nnnn',),
  'short': ('Cvcn',)
}

ALIASES = {
    'x': 'maximum',
    'max': 'maximum',
    'l': 'long',
    'm': 'medium',
    'med': 'medium',
    'b': 'basic',
    's': 'short',
    'i': 'pin',
    'n': 'name',
    'p': 'phrase'
}


class MPWTemplate(tuple):
    reg = DEFAULT_TEMPLATES.copy()
    chars = DEFAULT_CHARS.copy()
    aliases = ALIASES.copy()

    def __new__(cls, name):
        name = decode_if(name)
        return cls.reg[cls.aliases.get(name, name)]

    @classmethod
    def create(cls, name, templates):
        name = decode_if(name)
        try:
            return cls.reg[name]
        except KeyError:
            pass
        if isinstance(templates, (str, bytes, bytearray)):
            templates = (templates,)
        self = tuple.__new__(cls, map(decode_if, templates))
        cls.reg[name] = self
        return self

    @classmethod
    def get(cls, template):
        try:
            return cls(template)
        except KeyError:
            pass
        if isinstance(template, (str, bytes, bytearray)):
            template = (template,)
        return tuple(map(decode_if, template))

    @classmethod
    def char(cls, c, value=None):
        if value is None:
            return cls.chars[c]
        cls.chars[c] = value
        return value

    @classmethod
    def reset(cls):
        cls.reg = DEFAULT_TEMPLATES.copy()
        cls.chars = DEFAULT_CHARS.copy()


class MPWNameSpace(tuple):
    reg = {}

    def __new__(cls, name):
        return cls.reg[decode_if(name)]

    @classmethod
    def create(cls, name, password=None, login=None, answer=None):
        name_e = encode_if(name)
        name_d = decode_if(name)
        try:
            return cls.reg[name_d]
        except KeyError:
            pass
        if password is None:
            password = name_e
        if login is None:
            login = name_e + b'.login'
        if answer is None:
            answer = name_e + b'.answer'
        self = tuple.__new__(cls, (name_e, password, login, answer))
        cls.reg[name_d] = self
        return self

    @property
    def name(self):
        return self[0]

    @property
    def password(self):
        return self[1]

    @property
    def login(self):
        return self[2]

    @property
    def answer(self):
        return self[3]

    def __repr__(self):
        return '{}({!r})'.format(
            getattr(type(self), '__qualname__', type(self).__name__),
            self.name.decode())

default = MPWNameSpace.create('com.lyndir.masterpassword')
