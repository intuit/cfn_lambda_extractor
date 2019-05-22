import unittest

import test_cfn_example_lambda0

class Test(unittest.TestCase):
    def test(self):
        result = test_cfn_example_lambda0.handler({"bar": "baz"}, {})
        self.assertEqual(result, "foo-baz")

if __name__ == '__main__':
    unittest.main()
