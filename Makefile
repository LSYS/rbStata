.DEFAULT_GOAL := help

.PHONY: test
test: ## Run tests with pytest and coverage
	@echo "+ $@"
	-mkdir temp
	coverage erase
	coverage run -m pytest -v
	coverage report -m
	@rm -rf temp

.PHONY: lint
MYPY_OPTS := --ignore-missing-imports
BLACK_OPTS := --line-length 80
lint: ## Check with mypy, pyflakes, black
	@echo "+ $@"
# 	black setup.py $(BLACK_OPTS)
# 	black wbStata/*.py $(BLACK_OPTS)
# 	black tests/*.py $(BLACK_OPTS)
	mypy wbStata/*.py $(MYPY_OPTS)
# 	python -m pyflakes wbStata/*.py
# 	python -m pyflakes tests/*.py

.PHONY: clean-test
clean-test: ## Remove testing and coverage artifacts
	@echo "+ $@"
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf coverage.xml

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean-mypy
clean-mypy: ## Remove mypy artifacts	
	@echo "+ $@"
	@rm -rf .mypy_cache

.PHONY: clean-build
clean-build: ## Remove build artifacts
	@echo "+ $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info
	@rm -fr *.egg

.PHONY: clean-ipynb
clean-ipynb: ## Remove ipynb artifacts
	@echo "+ $@"
	@rm -fr *.ipynb_checkpoints

.PHONY: clean
clean: ## Remove artifacts
clean: clean-test clean-ipynb clean-mypy clean-pyc clean-build

.PHONY: build
build: clean ## Prepare packaging for PyPi
	@echo "+ $@"
	@rm -rf dist/ wbStata.egg-info/
	@python setup.py sdist
	twine check dist/*

.PHONY: setup
setup: ## Set up dependencies
	@echo "+ $@"
	@pip install -r tests/requirements_dev.txt
	@pip install -r requirements.txt

.PHONY: devtest
devtest: ## Install dev and test in editable mode
	@echo "+ $@"
	pip install -e .
	wbstata

.PHONY: help
help: ## Show this help message and exit
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'