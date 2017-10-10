#!/usr/bin/env python

import os
import sys
import argparse
import getpass

_PACKAGE_DIR = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)
)
# Ensure that the import can happen correctly
sys.path.insert(0, _PACKAGE_DIR)

try:
    import master_password
finally:
    sys.path.pop(0)

_ENV = {
    'name': 'MP_FULLNAME',
    'template': 'MP_SITETYPE',
    'counter': 'MP_SITECOUNTER',
    'version': 'MP_ALGORITHM'
}

if sys.version_info < (3,):
    input = raw_input


def _getpass(prompt='Your master password: ', confirm_prompt=None,
             error='Does not match!\n'):
    if confirm_prompt is None:
        confirm_prompt = 'Confirm ' + prompt.lower()
    while True:
        first = getpass.getpass(prompt)
        if getpass.getpass(confirm_prompt) == first:
            return first
        print(error)


_HELP = {
    'name': (
        'R|'
        'Specify the full name of the user.\n'
        '    Defaults to {env[name]} in env or prompts.'
    ).format(env=_ENV),
    'type': (
        'R|'
        'Specify the password\'s template.\n'
        '    Defaults to {env[template]} in env or '
        '\'long\' for password, \'name\' for login.\n'
        '        x, max, maximum | 20 characters, contains symbols.\n'
        '        l, long         | '
        'Copy-friendly, 14 characters, contains symbols.\n'
        '        m, med, medium  | '
        'Copy-friendly, 8 characters, contains symbols.\n'
        '        b, basic        | 8 characters, no symbols.\n'
        '        s, short        | Copy-friendly, 4 characters, no symbols.\n'
        '        i, pin          | 4 numbers.\n'
        '        n, name         | 9 letter name.\n'
        '        p, phrase       | 20 character sentence.'
    ).format(env=_ENV),
    'counter': (
        'R|'
        'The value of the counter.\n'
        '    Defaults to {env[counter]} in env or 1.'
    ).format(env=_ENV),
    'version': (
        'R|'
        'The algorithm version to use.\n'
        '    Defaults to {env[version]} in env or 3.'
    ).format(env=_ENV),
    'variant': (
        'R|'
        'The kind of content to generate.\n'
        '    Defaults to \'password\'.\n'
        '        p, password | The password to log in with.\n'
        '        l, login    | The username to log in as.\n'
        '        a, answer   | The answer to a security question.'
    ),
    'context': (
        'R|'
        'A variant-specific context.\n'
        '    Defaults to empty.\n'
        '        Empty for a universal site answer or\n'
        '        the most significant word(s) of the question.'
    ),
    'site': 'The site to generate a password for.',
    'identicon': (
        'Disables the identicon, which are 4 characters generated from '
        'your full name and password which are different for different '
        'names and passwords. Helps spot typos.'
    )
}


_TYPE_CHOICES = (
    tuple(master_password.datatypes.ALIASES.keys()) +
    tuple(master_password.datatypes.ALIASES.values())
)

_VERSION_CHOICES = (0, 1, 2, 3)


class RawFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Master Password CLI',
                                     prog='master_password',
                                     formatter_class=RawFormatter)
    parser.add_argument('-u', metavar='name', help=_HELP['name'],
                        default=os.environ.get(_ENV['name']))
    type_default = os.environ.get(_ENV['template'], '').strip().lower()
    if type_default not in _TYPE_CHOICES:
        type_default = None
    parser.add_argument('-t', metavar='type', help=_HELP['type'],
                        choices=_TYPE_CHOICES, default=type_default)
    counter_default = os.environ.get(_ENV['counter'], 1)
    try:
        counter_default = int(counter_default)
    except ValueError:
        counter_default = 1
    parser.add_argument('-c', metavar='counter', help=_HELP['counter'],
                        type=int, default=counter_default)
    version_default = os.environ.get(_ENV['version'], 3)
    try:
        version_default = int(version_default)
        if version_default not in _VERSION_CHOICES:
            version_default = 3
    except ValueError:
        version_default = 3
    parser.add_argument('-a', metavar='version', help=_HELP['version'],
                        type=int, default=version_default,
                        choices=_VERSION_CHOICES)
    parser.add_argument('-V', metavar='variant', help=_HELP['variant'],
                        default='password', choices=(
            'p', 'password', 'l', 'login', 'a', 'answer'
        ))
    parser.add_argument('-C', metavar='context', help=_HELP['context'],
                        default=None)
    parser.add_argument('site', help=_HELP['site'], nargs='?', default=None)
    parser.add_argument('-i', help=_HELP['identicon'], action='store_false')

    parser.add_argument('-P', metavar='password', help=argparse.SUPPRESS,
                        default=None)

    args = parser.parse_args(argv)

    full_name = args.u
    template = args.t
    counter = args.c
    version = args.a
    namespace = args.V
    context = args.C
    site = args.site

    mpw = args.P  # Do not use. Insecure. For testing purposes only.

    if full_name is None:
        full_name = input('Your full name: ')
    if site is None:
        site = input('Site name: ')

    namespace = {
        'p': 'password', 'password': 'password', 'l': 'login', 'login': 'login',
        'a': 'answer', 'answer': 'answer'
    }[namespace]

    if template is None:
        template = {
            'password': 'long', 'login': 'name', 'answer': 'phrase'
        }[namespace]

    debug = mpw is not None
    if debug:
        print(args)
        print('Full name: ' + repr(full_name))
        print('Template: ' + repr(template))
        print('Counter: ' + repr(counter))
        print('Version: ' + repr(version))
        print('Namespace: ' + repr(namespace))
        print('Context: ' + repr(context))
        print('Site: ' + repr(site))
        print('Password: ' + repr(mpw))
    else:
        mpw = _getpass()

    sys.stdout.write('{}\'s password for {}:\n'.format(full_name, site))

    if args.i:
        identicon = master_password.MPW.identicon(full_name, mpw)

        if debug:
            print('Identicon: ' + repr(identicon.encode('utf-8')) + '\n')

        try:
            sys.stdout.write(u'[ {} ]: '.format(identicon))
        except UnicodeError as e:
            sys.stderr.write(
                '\nError writing identicon: {}\n'.format(e) +
                'Please pass the -i argument to avoid attempting to '
                'display the identicon.\n'
            )
        sys.stdout.flush()

    mpw = master_password.MPW(full_name, mpw, version=version)

    print(mpw.generate(site, counter, context, template, namespace))

    if debug:
        print('Key: ' + repr(mpw.key))
        print('Seed: ' + repr(mpw.seed(site, namespace, counter, context)))


if __name__ == '__main__':
    main(sys.argv[1:])
