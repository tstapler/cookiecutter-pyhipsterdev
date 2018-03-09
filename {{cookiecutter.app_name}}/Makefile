# REPO_OWNER name and PROJECT_NAME must be lowercase
REPO_OWNER={{cookiecutter.github_project_owner}}
PROJECT_NAME={{cookiecutter.app_name}}

IMAGE_TAG=$(REPO_OWNER)/$(PROJECT_NAME)_dev

SOURCE_CODE={{cookiecutter.app_name}} tests

# Build the docker container
DOCKER_BUILD=docker build . -t $(IMAGE_TAG)

# Ensure the container is built and execute a command in it
DOCKER_RUN=$(DOCKER_BUILD) && docker run -it -v $(CURDIR):/$(PROJECT_NAME) $(IMAGE_TAG) sh -c

# Activate the virtualenv created by Pipenv
RUNP=. /root/.local/share/virtualenvs/pip-*/bin/activate &&

# Run before every command executed in the container
DOCKER_PRETASK=$(RUNP) cd /$(PROJECT_NAME) && make local-format

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

deps: ## Install runtime dependencies
	pipenv install 

dev-deps: ## Install development dependencies
	pipenv install --dev

# All of the rules with the "local-" prefix are not run in a docker container
# To execute 'local-{name}' rules in the docker container add '{name}' to DOCKER_RULES.
DOCKER_RULES := $(DOCKER_RULES) lock-deps
local-lock-deps: ## Lock the dependencies of the project
	pipenv lock --requirements  > requirements.txt
	pipenv lock --requirements --dev > requirements_dev.txt

DOCKER_RULES := $(DOCKER_RULES) ready

local-ready: local-test-all local-create-cfn local-update-docs {% if cookiecutter.cloudformation %}local-check-cfn {% endif %}local-lock-deps ## Format and test all code
	@echo "All checks pass. You're ready to commit!"

DOCKER_RULES := $(DOCKER_RULES) coverage
local-coverage: ## Check code coverage quickly with the default Python
	coverage run --source $(PROJECT_NAME) setup.py test
	coverage report -m

DOCKER_RULES := $(DOCKER_RULES) coverage-view
local-coverage-view: coverage # Open a test coverage map in your browser
	coverage html
	open htmlcov/index.html

{% if cookiecutter.cloudformation %}
DOCKER_RULES := $(DOCKER_RULES) check-cfn
local-check-cfn: local-create-cfn ## Validate the cloud formation scripts
	@cf-check cloudformation/*.yml
{% endif %}

DOCKER_RULES := $(DOCKER_RULES) check-format
local-check-format: ## Throw an error if project files need formatting changes
	 @{ [ ! "$(shell yapf --recursive --diff $(SOURCE_CODE))" ]  && \
	 [ ! "$(shell isort --check-only --ignore-whitespace --recursive | grep "ERROR")" ]; } || \
	 { echo "Please run 'make format' to fix incorrect formatting" && exit 1; }
	@echo "All python files are properly formatted"

DOCKER_RULES := $(DOCKER_RULES) format
local-format: ## Automatically format code using yapf and isort
	@echo "Formatting to fit style guide"
	@yapf --recursive --in-place $(SOURCE_CODE)
	@isort --apply --atomic --recursive

DOCKER_RULES := $(DOCKER_RULES) test
local-test: ## Run linter, coverage, and unit tests
	py.test -x --pdb tests

DOCKER_RULES := $(DOCKER_RULES) test-watch
local-test-watch: ## Run the unit tests on filechanges
	py.test --looponfail tests

DOCKER_RULES := $(DOCKER_RULES) test-all
local-test-all: local-lock-deps ## Run the tests on both python 2.7 and 3.6
	tox

DOCKER_RULES := $(DOCKER_RULES) update-docs
local-update-docs: ## Update the documentation
	md-magic --config ./markdown.config.js

DOCKER_RULES := $(DOCKER_RULES) shell
local-shell: ## Open a shell in the project's docker container
	{% if cookiecutter.cli_app %}pip install -e . && {% endif %}bash

# Ignore files/directories with the same name as the target ex: "test"
.PHONY: $(DOCKER_RULES)
# When 'make test' is run, the Makefile will run 'make local-test' in the docker container
$(DOCKER_RULES):
	$(RUN_LOCAL_COMMAND_IN_DOCKER)
