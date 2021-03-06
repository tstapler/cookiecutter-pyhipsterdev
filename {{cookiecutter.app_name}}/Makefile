# REPO_OWNER name and PROJECT_NAME must be lowercase
REPO_OWNER={{cookiecutter.github_project_owner}}
PROJECT_NAME={{cookiecutter.app_name}}

IMAGE_TAG=$(REPO_OWNER)/$(PROJECT_NAME)_dev

SOURCE_CODE=$(shell find {{cookiecutter.app_name}} tests setup.py -name \*.py -type f)

PIP_INDEX_URL="$$(grep "@pypi" ~/.pip/pip.conf | awk '{print $$3}')"

# Build the docker container
DOCKER_BUILD=docker build . -t $(IMAGE_TAG){% if cookiecutter.include_pypi_config == "true" %} \
	     --build-arg PIP_INDEX_URL="$$(grep "@pypi" ~/.pip/pip.conf | awk '{print $$3}')"
		{%- endif %}

# Ensure the container is built and execute a command in it
DOCKER_RUN=$(DOCKER_BUILD) && docker run -it -v $(CURDIR):/$(PROJECT_NAME) $(IMAGE_TAG) sh -c

# Run before every command executed in the container
DOCKER_PRETASK=cd /$(PROJECT_NAME) && make local-format

# Run run local make target in a docker container ex: check-cfn -> local-checkcfn
RUN_LOCAL_COMMAND_IN_DOCKER=$(DOCKER_RUN) "$(DOCKER_PRETASK) && make local-$@"

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | \
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' | \
	sed "s/local-//" | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc ## Remove build artifacts and python artifacts

clean-build: ## Remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## Remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

update-template: ## Update the cookiecutter template (Overrides upstaged changes)
	cookiecutter gh:tstapler/cookiecutter-pyhipsterdev --output-dir .. --config-file .cookiecutter.yaml --no-input --overwrite-if-exists
# Template update command taken from https://github.com/audreyr/cookiecutter/issues/784

# All of the rules with the "local-" prefix are not run in a docker container
# To execute 'local-{name}' rules in the docker container add '{name}' to DOCKER_RULES.
DOCKER_RULES := $(DOCKER_RULES) ready
local-ready: local-test local-update-docs {% if cookiecutter.cloudformation == "true" %}local-check-cfn {% endif %}## Format and test all code
	@echo "All checks pass. You're ready to commit!"

DOCKER_RULES := $(DOCKER_RULES) coverage
local-coverage: ## Check code coverage quickly with the default Python
	coverage run --source $(PROJECT_NAME) setup.py test
	coverage report -m

DOCKER_RULES := $(DOCKER_RULES) coverage-view
local-coverage-view: local-coverage local-test # Open a test coverage map in your browser
	coverage html
	open htmlcov/index.html

{% if cookiecutter.cloudformation == "true" -%}
DOCKER_RULES := $(DOCKER_RULES) check-cfn
local-check-cfn: ## Validate the cloud formation scripts
	@cf-check cloudformation/*.yml
{%- endif -%}

DOCKER_RULES := $(DOCKER_RULES) check-format
local-check-format: ## Throw an error if project files need formatting changes
	 @{ [ ! "$(shell yapf --recursive --diff $(SOURCE_CODE))" ]  && \
	 [ ! "$(shell isort --check-only --ignore-whitespace --recursive | grep "ERROR")" ] && [ ! $(shell unify --check $(SOURCE_CODE)) ]; } || \
	 { echo "Please run 'make format' to fix incorrect formatting" && exit 1; }
	@echo "All python files are properly formatted"

DOCKER_RULES := $(DOCKER_RULES) package
local-package: ## Generate packaging
	python setup.py bdist_wheel

DOCKER_RULES := $(DOCKER_RULES) format
local-format: ## Automatically format code using yapf and isort
	@echo "Formatting to fit style guide"
	@yapf --recursive --in-place $(SOURCE_CODE)
	@isort --apply --atomic --recursive
	@unify  --in-place $(SOURCE_CODE)

DOCKER_RULES := $(DOCKER_RULES) test
local-test: ## Run linter, coverage, and unit tests
	py.test -x tests

DOCKER_RULES := $(DOCKER_RULES) debug
local-debug: ## Run linter, coverage, and debug unit tests
	py.test -x --pdb tests

DOCKER_RULES := $(DOCKER_RULES) test-watch
local-test-watch: ## Run the unit tests on filechanges
	py.test --looponfail tests

DOCKER_RULES := $(DOCKER_RULES) update-docs
local-update-docs: ## Update the documentation
	md-magic --config ./markdown.config.js

DOCKER_RULES := $(DOCKER_RULES) shell
local-shell: ## Open a shell in the project's docker container
	bash

# Ignore files/directories with the same name as the target ex: "test"
.PHONY: $(DOCKER_RULES)
# When 'make test' is run, the Makefile will run 'make local-test' in the docker container
$(DOCKER_RULES):
	$(RUN_LOCAL_COMMAND_IN_DOCKER)
