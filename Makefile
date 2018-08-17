VENV := .venv

default: validate

validate: lint test generate-documentation freeze-requirements

generate-documentation:
	sphinx-apidoc -o docs/source/ moe
	rm docs/source/moe.rst # remove unused rst file
	make -C docs html

freeze-requirements:
	pip freeze > config/requirements.txt

test:
	pytest

lint: pylint flake8

pylint:
	pylint -E --rcfile config/.pylintrc moe tests

flake8:
	flake8 --config=config/.flake8 moe tests

show-documentation:
	google-chrome docs/build/html/index.html

.PHONY: default validate generate-documentation freeze-requirements test lint pylint flake8 show-documentation
