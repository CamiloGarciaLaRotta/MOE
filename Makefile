VENV := .venv

default: validate

validate: lint test vulnerabilities generate-documentation freeze-requirements

generate-documentation:
	@echo -e "\nGenerating documentation..."
	sphinx-apidoc -o docs/source/ moe
	rm docs/source/moe.rst # remove unused rst file
	make -C docs html

freeze-requirements:
	@echo -e "\nFreezing requirements..."
	pip freeze > config/requirements.txt

vulnerabilities:
	@echo -e "\nChecking for vulnerabilities..."
	bandit -r moe --format custom --msg-template "{relpath:20.20s}: {line:03}: {test_id:^8}: DEFECT: {msg:>20}" -ll -i

test:
	pytest
	pytest --cov=moe tests/

lint: pylint flake8

pylint:
	pylint -E --rcfile config/.pylintrc moe tests

flake8:
	flake8 --config=config/.flake8 moe tests

show-documentation:
	@echo -e "\nOpening documentation in browser..."
	google-chrome docs/build/html/index.html

.PHONY: default validate generate-documentation freeze-requirements test vulnerabilities lint pylint flake8 show-documentation
