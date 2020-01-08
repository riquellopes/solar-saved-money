.SILENT:

venv:
	pyenv virtualenv 3.8.0 saved
	pyenv activate saved

setup:venv
	pip3 install -U pip3
	pip3 install -r requirements-dev.txt

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

run:
	python main.py

test:clean
	PYTHONPATH=save_money pytest -s -v --cov=save_money --cov-report term-missing tests/${path}