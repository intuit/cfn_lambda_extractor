#!/bin/bash

set -e 

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cfn_lambda_extractor \
    -c cfn.yaml \
    -o $DIR \
    -p test_cfn_example_lambda \
    -s ValueToSub1="'foo'"

python3 $DIR/test.py
