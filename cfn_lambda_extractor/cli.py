#!/usr/bin/env python3

import argparse
import logging
import sys

from cfn_lambda_extractor import cfn_lambda_extractor

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cfn-template",
        help="Cloudformation template to update.",
        dest="cfn_template",
        required=True)
parser.add_argument("-l", "--log-level",
        help="[DEBUG|INFO|WARN|CRITICAL]",
        dest="log_level",
        default="INFO")
parser.add_argument("-o", "--output",
        help="Directory to write output",
        dest="output_dir",
        required=True)
parser.add_argument("-p", "--prefix",
        help="String to prefix function names",
        dest="prefix",
        default="tmp_test_lambda_function")
parser.add_argument("-s", "--substitution_values",
        help="CSV, equals seperated substitution values to replace ${} style cfn subs.",
        dest="substitution_values",
        default="")
args = parser.parse_args()

logging.basicConfig(level=getattr(logging, args.log_level.upper()))

def write_functions(fns):
    for name,v in fns.items():
        file_name = args.prefix + name + ".py"
        output = args.output_dir + "/" + file_name
        logging.info("Writing function '{}' to '{}'.".format(name, output))
        f = open(output, "w")
        f.write(v)
        f.close()

def run():
    try:
        cfn_template_data = cfn_lambda_extractor.load_input_file(args.cfn_template)
        values = cfn_lambda_extractor.parse_csv_input_values(args.substitution_values)
        fns = cfn_lambda_extractor.extract_functions(cfn_template_data, values)
        write_functions(fns)
        logging.info("Completed processing cfn template.")
    except Exception as e:
        logging.exception("Received error '{}'.".format(str(e)))
        sys.exit(1)
