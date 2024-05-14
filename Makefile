PROJECT_NAME = arctic_code_assistan_env
VENV_NAME = .venv/${PROJECT_NAME}_env
PYTHON = ${VENV_NAME}/bin/python
PIP = ${VENV_NAME}/bin/pip

.PHONY: clean test dist docs

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "dist - package the distribution"
	@echo "docs - generate Sphinx HTML documentation, including API docs"

test: ## Run tests
	$(PYTHON) -m unittest discover

lint: ## Lint the project
	$(VENV_NAME)/bin/flake8 .

format: ## Format the code
	$(VENV_NAME)/bin/black .

run: ## Run the main application
	$(PYTHON) main.py

clean: ## Remove python artifacts and virtualenv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	rm -rf $(VENV_NAME)
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build

requirements: ## Freeze the current state of the environment to requirements.txt
	$(PIP) freeze > requirements.txt

deploy: ## Deploy to your platform (example purpose, you need to customize this)
	echo "Replace this placeholder with your deploy logic"

venv:
	conda create -p $(VENV_NAME) python=3.10 --yes

install: venv
	$(VENV_NAME)/bin/pip install -r requirements.txt
	
venv_activate:
	source $(VENV_NAME)/bin/activate