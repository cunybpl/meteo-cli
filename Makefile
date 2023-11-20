

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/


test: clean-test
	poetry run pytest -s -v --cov=meteo_cli/ --cov-report=term-missing && mypy meteo_cli --strict

test-single-module: clean-test
	poetry run pytest --cov=meteo_cli/ --cov-report=term-missing ${module} -v -s && mypy meteo_cli --strict
	