import logging
import os
import re
import tempfile
import unittest

import cfn_lambda_extractor

class Test(unittest.TestCase):
    def setUp(self):
        d = os.path.dirname(os.path.realpath(__file__))
        self.testdata_dir = d + "/testdata/"
        test_template = self.testdata_dir + "test_template.yaml"
        self.data = cfn_lambda_extractor.load_input_file(test_template)

    def test_template_extraction(self):
        values = {"ValueToSub1": "test1234","ValueToSub2": "test4321"}
        fns = cfn_lambda_extractor.extract_functions(self.data, values)

        efn1 = open(self.testdata_dir + "expected_output_fn1.py")
        expected_output_fn1 = efn1.read()
        efn1.close()

        efn2 = open(self.testdata_dir + "expected_output_fn2.py")
        expected_output_fn2 = efn2.read()
        efn2.close()

        self.assertEqual("".join(fns["1"]), expected_output_fn2.rstrip('\n'))
        self.assertEqual("".join(fns["0"]), expected_output_fn1.rstrip('\n'))

    def test_value_not_provided(self):
        with self.assertRaises(Exception) as e:
            cfn_lambda_extractor.extract_functions(self.data, {})
        err = str(e.exception)
        self.assertTrue(re.match("Value 'ValueToSub.' not provided.", err))

    def test_no_resources(self):
        with self.assertRaises(Exception) as e:
            cfn_lambda_extractor.extract_functions("", {})
        self.assertEqual(str(e.exception), "No Resources in template.")

    def test_parse_input(self):
        self.assertEqual(cfn_lambda_extractor.parse_csv_input_values("a=1,b=2"), {"a":'1', "b":'2'})

    def test_replace_values_in_line(self):
        s = "name = ${AccountId}-${Region}"
        v = {"AccountId": "123443211234", "Region": "us-west-2"}
        self.assertEqual(cfn_lambda_extractor.replace_values_in_line(s, v), "name = 123443211234-us-west-2")

logging.basicConfig(level=logging.CRITICAL)

if __name__ == '__main__':
    unittest.main()
