.SILENT:
PIP=.venv/bin/pip
PYTEST=.venv/bin/pytest
PYTHON=.venv/bin/python

venv:
	virtualenv .venv --python=python3

setup:venv
	${PIP} install -U pip
	${PIP} install -r requirements-dev.txt

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

run:
	${PYTHON} main.py