# example

I am an example of extracting, replacing variables and testing a lambda function from a 
Cloudformation template.

To use, run **test.sh**.

```
$ bash test.sh
INFO:root:Loading input from file 'cfn.yaml'.
INFO:root:Loaded 1 function(s).
INFO:root:Replacing cfn value 'ValueToSub1' with ''foo''.
INFO:root:Writing function '0' to '/Users/bweaver/code/cfn_lambda_extractor/example/test_cfn_example_lambda0.py'.
INFO:root:Completed processing cfn template.
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
