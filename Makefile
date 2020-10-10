all: test

clean:
	\rm -f dist/*

test: clean; python -m unittest discover cfn_lambda_extractor/

.PHONY: clean test
