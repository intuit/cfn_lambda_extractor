#!/usr/bin/env python

VERSION='1.0.0'

from distutils.core import setup

setup(name='intuit.cfn_lambda_extractor',
      version=VERSION,
      description='Extract embeded AWS Lambda functions from Cloudformation templates.',
      author='Brett Weaver',
      author_email='brett_weaver@intuit.com',
      packages=['cfn_lambda_extractor'],
      url='https://github.com/intuit/cfn_lambda_extractor',
      entry_points = {
          'console_scripts': [
              'cfn_lambda_extractor = cfn_lambda_extractor.cli:run'
              ]
          }
     )
