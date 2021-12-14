import unittest


class TestProgram(unittest.TestCase):
    def test_getname(self):
        from classes import User
        name = 'Leroy Jenkins'
        user = User('cb36d417-4a9c-4769-99f9-e20cffb8a026', name)
        self.assertEqual(user.get_name(), name)


    def test_splitdiff_calc(self):
        from functions import split_diff
        diff_mins = 40
        diff_hours = 15
        diff_days = 3
        diff = (diff_days * (24 * 60)) + (diff_hours * 60) + diff_mins
        self.assertEqual(split_diff(diff), (diff_days, diff_hours, diff_mins))
    
    def test_splitdiff_type(self):
        from classes import User
        from functions import split_diff
        from exceptions import DiffTypeError
        with self.assertRaises(DiffTypeError):
            split_diff('text')
            split_diff(20.3)
            split_diff(20)
            split_diff(['one', 2, {'three', '9'}, 'четыре', '五'])
            split_diff(('this parameter is not an integer', 'this one isn\'t either'))
            split_diff(lambda x: x * x)
            split_diff({'key': 'value'})
            split_diff(User('cb36d417-4a9c-4769-99f9-e20cffb8a026', 'Leroy Jenkins'))
            split_diff(b'\x34\x32\x30\x42\x4c\x41\x5a\x45\x49\x54')


if __name__ == '__main__':
    unittest.main(verbosity=2)
