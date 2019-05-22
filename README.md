# cfn_lambda_extractor

AWS Cloudformation extracts [inline Lambda function code](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html)
from a Cloudformation template.

For example, see the below **TestFunction1** Lambda function:

```yaml
TestFunction1:
  Type: AWS::Lambda::Function
  Properties:
    Code:
      ZipFile: !Sub
        - |
          def handler(event, context):
              val = ${ValueToSub1}
              print("This is a test with value '{}'.".format(val))
        - ValueToSub1: "test1234"
    Handler: index.handler
    Role: !GetAtt MyRole.Arn
    Runtime: python3.6
```

Inline code is great for incorporating code directly within your Cloudformation templates, however
the code is difficult to test.

To support extracting and testing code included in your Cloudformation template, **cfn_lambda_extractor**
will parse your AWS Cloudformation templates, remove inline code, replace variables
populated by **${variable}** styble [sub](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-sub.html)
statements, and write the modified template to a directory for testing.

See [example](https://github.com/intuit/cfn_lambda_extractor/tree/master/example) directory for a full working
example of extracting, replacing variables and finally testing inline Lambda code.

## Installation

To install directly from GitHub.

```shell
pip3 install git+https://github.com/intuit/cfn_lambda_extractor
```
## Usage

To extract all the functions in **template.yaml** into **/tmp**:

```
$ cfn_lambda_extractor -c template.yaml -o /tmp
INFO:root:Loading input from file 'template.yaml'.
INFO:root:Loaded 2 function(s).
INFO:root:Writing function '0' to '/tmp/tmp_test_lambda_function0.py'.
INFO:root:Writing function '1' to '/tmp/tmp_test_lambda_function1.py'.
INFO:root:Completed processing cfn template.
```

This will result in a file being created for each function.

For example:

```
$ ls /tmp/*.py
tmp_test_lambda_function0.py
tmp_test_lambda_function1.py
```

Variable substituation for Cloudformation substituation of variables in the form
of **${VARIABLE}** is supported.  You can include a list of variables to replace as
a command line argument.

```
$ cfn_lambda_extractor -c template.yaml -o /tmp -s Key1=test1234,Key2=test4321
INFO:root:Loading input from file 'cfn_lambda_extractor/testdata/test_template.yaml'.
INFO:root:Loaded 2 function(s).
INFO:root:Replacing cfn value 'Key1' with 'test1234'.
INFO:root:Replacing cfn value 'Key2' with 'test4321'.
INFO:root:Writing function '0' to '/tmp/tmp_test_lambda_function0.py'.
INFO:root:Writing function '1' to '/tmp/tmp_test_lambda_function1.py'.
INFO:root:Completed processing cfn template.
```

## Development

### Test

```
make test
```

## Constraints and Known Limitations

Lots of opportunity to improve me...

* Only supports YAML.
* Only supports Python functions.
* Only supports replacement of ${VAR} style cfn substituation (not Fn::Sub style or other variables).
* No other psuedo parameters or replacements.

Copyright (c) 2019 Intuit
