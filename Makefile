.DEFAULT_GOAL := help

.PHONY: test
test: ## Run tests with pytest and coverage
test: 
	-mkdir temp
	coverage erase
	coverage run -m pytest -v
	coverage report -m
	@rm -rf temp

.PHONY: lint
lint: ## Check with mypy, pyflakes, black
lint: 
	black wbStata/*.py 
	black tests/*.py 
	mypy wbStata/*.py --ignore-missing-imports
	python -m pyflakes wbStata/*.py
	python -m pyflakes tests/*.py

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean-mypy
clean-mypy: ## Remove mypy artifacts	
	@rm -rf .mypy_cache

.PHONY: clean-build
clean-build: ## Remove build artifacts
	@echo "+ $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

.PHONY: clean
clean: ## Remove artifacts
clean: clean-mypy clean-pyc clean-build

.PHONY: setup
setup: ## Set up env and requirements
setup:
	$(CONDA_ACTIVATE) wbStata
# 	conda activate 


.PHONY: install
install: ## Install for internal testing
install:
	@rm -rf dist/ runpynb.egg-info/
	@python setup.py sdist
	tar -xf dist/runpynb-0.1.*.tar.gz
	python ./assets/checkDistCR.py
	twine check dist/*

.PHONY: devtest
devtest:	
	pip install -e .
	wbstata

.PHONY: help
help: ## Show this help message and exit
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'