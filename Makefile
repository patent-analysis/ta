.PHONY: help init clean test validate mock create delete info deploy
.DEFAULT_GOAL := help
environment = "inlined"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: 	## install the requirments
	@pip3 install -r requirements_local.txt 

lint:	## run the flake8 linter
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test: ## run the unit tests
	@pytest -v -s tests

stack-up: ## run the local aws stack environment
	cd ./localstack; ./start.sh

stack-down: ## stop the local aws stack environment
	cd ./localstack; docker-compose down

run-local: ## build and invoke the lambda function
	@echo "cleaning all stale docker images and containers...."
	docker image prune -f
	docker container prune -f
	sam build
	sam local invoke --parameter-overrides 'KeyPairName=MyKey LOCAL_ENV=true'  -e ./events/process_document_event.json

debug-local: ## build and invoke the lambda function in debug mode
	docker image prune -f
	docker container prune -f
	sam build
	sam local invoke --parameter-overrides 'KeyPairName=MyKey LOCAL_ENV=true'  -e ./events/process_document_event.json -d


build-stack: ## builds the application (docker images)
	sam build

deploy-stack: ## deploy the stack using AWS SAM
	@echo "TODO...."