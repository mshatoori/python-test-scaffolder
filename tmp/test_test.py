import unittest

from guinea_pig import function_to_be_tested


class MyTestCase(unittest.TestCase):
    def test_something(self):
        """This test function tests something when these conditions are met:
        - CONDITION1
        - CONDITION2
        """

        in_out_list = [
            # TODO: Fill with input output pairs in form of "((args, kwargs), return_val)"
            # TODO: These values should cover all edge cases and stuff...
        ]

        for (args, kwargs), return_val in in_out_list:
            real_return_val = function_to_be_tested(*args, **kwargs)
            self.assertEqual(return_val, real_return_val)


if __name__ == '__main__':
    unittest.main()
