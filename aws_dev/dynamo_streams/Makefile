
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

deploydev: ## deploy in dev
	cd terraform && terraform init && terraform fmt && terraform validate ; \
	terraform workspace select dev || terraform workspace new dev ; \
	terraform plan -input=false -var-file=tfvars/dev.tfvars -out=devplan.tfplan ; \
	terraform apply devplan.tfplan

deployprod: ## deploy in prod
	cd terraform && terraform init && terraform fmt && terraform validate ; \
	terraform workspace select prod || terraform workspace new prod ; \
	terraform plan -input=false -var-file=tfvars/prod.tfvars -out=prodplan.tfplan ; \
	terraform apply prodplan.tfplan

destroydev: ## destroy in dev
	cd terraform ; \
	terraform workspace select dev || terraform workspace new dev ; \
	terraform destroy -var-file=tfvars/dev.tfvars -auto-approve

destroyprod: ## destroy in prod
	cd terraform ; \
	terraform workspace select prod || terraform workspace new prod ; \
	terraform destroy -var-file=tfvars/prod.tfvars -auto-approve
