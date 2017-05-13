import os
import sys
import unittest

__all__ = ('MPWTest',)

__dir__ = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

try:
    from master_password import *
finally:
    sys.path.pop(0)


class MPWTest(unittest.TestCase):
    full_name = 'name'
    password = 'password'
    site = 'example.com'
    namespace = MPW_DEFAULT_NAMESPACE
    counter = 1
    template = 'long'
    context = 'test'

    expected_key = bytearray([
        162, 148, 87, 1, 5, 98, 177, 136, 173, 164, 61, 216, 248, 147, 240,
        167, 96, 170, 118, 14, 42, 255, 205, 206, 24, 138, 137, 221, 98,
        187, 80, 251, 103, 131, 82, 180, 119, 67, 200, 117, 221, 121, 170,
        207, 213, 42, 110, 89, 2, 96, 254, 185, 5, 93, 49, 4, 179, 102,
        101, 20, 152, 180, 113, 237
    ])
    expected_seed = bytearray([
        121, 18, 80, 226, 166, 124, 32, 87, 42, 135, 48, 57, 178, 121, 184, 83,
        4, 217, 140, 201, 125, 57, 241, 203, 182, 81, 172, 173, 177, 32, 35, 3
    ])
    expected_seed_w_context = bytearray([
        26, 95, 64, 176, 34, 161, 38, 253, 226, 47, 249, 49, 28, 96, 185, 236,
        74, 238, 48, 212, 142, 45, 238, 32, 191, 170, 108, 199, 238, 34, 160, 99
    ])
    expected_password = 'XaveYifb5@TovvZukaQatn3#XihmPafe'
    expected_password_w_context = 'PulrSoceHuko6^HukjDifoPedo9/Rath'
    expected_password_v_0 = 'MageRiqi5@XocuWunaMaxe3.MidiDaqe'
    expected_password_w_context_v_0 = 'DusnWokeZukk6.DunfPiqoDepq9]Naxz'

    def test_key_calculation(self):
        self.assertEqual(
            MPW.calculate_key(
                self.password,
                MPW.calculate_salt(
                    self.full_name, self.namespace
                )
            ), self.expected_key, 'Incorrect key calculated!')

    def test_seed_calculation(self):
        mpw = MPW.from_key(self.expected_key, self.full_name, self.namespace)
        self.assertEqual(
            mpw.seed(self.site, self.namespace, self.counter),
            self.expected_seed, 'Incorrect seed calculated!'
        )

    def test_seed_calculation_w_context(self):
        mpw = MPW.from_key(self.expected_key, self.full_name, self.namespace)
        self.assertEqual(
            mpw.seed(self.site, self.namespace, self.counter, self.context),
            self.expected_seed_w_context,
            'Incorrect seed calculated! (With context)'
        )

    def test_password_generation(self):
        mpw = MPW.from_key(self.expected_key, self.full_name, self.namespace)
        self.assertEqual(
            mpw.generate(self.site, self.counter, None,
                         self.template, self.namespace, True),
            self.expected_password,
            'Incorrect password generated!'
        )
        self.assertEqual(
            mpw.generate(self.site, self.counter, self.context,
                         self.template, self.namespace, True),
            self.expected_password_w_context,
            'Incorrect password generated! (With context)'
        )

    def test_password_generation_v_0(self):
        mpw = MPW.from_key(self.expected_key, self.full_name, self.namespace, 0)
        self.assertEqual(
            mpw.generate(self.site, self.counter, None,
                         self.template, self.namespace, True),
            self.expected_password_v_0,
            'Incorrect password generated! (Version 0)'
        )
        self.assertEqual(
            mpw.generate(self.site, self.counter, self.context,
                         self.template, self.namespace, True),
            self.expected_password_w_context_v_0,
            'Incorrect password generated! (With context; Version 0)'
        )


if __name__ == '__main__':
    unittest.main()
