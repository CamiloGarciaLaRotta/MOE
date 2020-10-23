VENV := .venv

default: validate

validate: lint test vulnerabilities freeze-requirements

freeze-requirements:
	@echo -e "\nFreezing requirements..."
	pip freeze > requirements.txt

vulnerabilities:
	@echo -e "\nChecking for vulnerabilities..."
	bandit -r moe --format custom --msg-template "{relpath:20.20s}: {line:03}: {test_id:^8}: DEFECT: {msg:>20}" -ll -i

test:
	PYTHONPATH=. pytest -v

lint: pylint flake8

pylint:
	pylint -E --rcfile .pylintrc moe tests

flake8:
	flake8 --config=.flake8 moe tests

.PHONY: default validate freeze-requirements test vulnerabilities lint pylint flake8
