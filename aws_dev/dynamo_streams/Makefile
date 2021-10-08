
help:
	@echo make targets:
	@awk ' \
	    BEGIN { FS=":.*?## " } \
	    $$1~/^[A-Za-z]/ && $$2~/^.+/ { \
	        printf "    * %-18.18s %s\n",$$1":",$$2 \
	    }' $(MAKEFILE_LIST)


lint:  ## check syntax of python code
	@echo "Checking Python code for syntax errors (fatal)"
	pipenv run pylint --errors-only src/*.py
	@echo "###############################"
	@echo "Checking Python code for syntax suggestions (non-fatal)"
	pipenv run pylint --exit-zero src/*.py

unittest: ## run pytest
	pipenv run python -m pytest -s -vvv tests/unit/