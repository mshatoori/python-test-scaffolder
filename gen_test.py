import unittest


class MyTestCase(unittest.TestCase):
    def test__internal_function_0(self):
        """This test function tests test__internal_function_0"""
        in_out_list = [
            # TODO: Fill with input output pairs in form of "((args, kwargs), return_val)"
            # TODO: These values should cover all edge cases and stuff...
        ]

        for (args, kwargs), return_val in in_out_list:
            real_return_val = test__internal_function_0(*args, **kwargs)
            self.assertEqual(return_val, real_return_val)


if __name__ == '__main__':
    unittest.main()
