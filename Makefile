all: test

clean:
	\rm -f dist/*

test: clean
	python3 cfn_lambda_extractor/test.py

.PHONY: clean test
