TEST_DIR := tests/

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

coverage:
	pdm run coverage run -m pytest $(TEST_DIR)
	pdm run coverage report -m
	pdm run coverage html

lint:
	pdm run pylint --exclude=.tox

test:
	pdm run pytest --verbose --color=yes $(TEST_DIR)

clean-docs:
	rm -rf docs/build/

docs: clean-docs
	pdm run sphinx-build -b doctest docs/source/ docs/build/
	pdm run sphinx-build -b html docs/source/ docs/build/

serve-coverage:
	python3 -m http.server --directory htmlcov/ 8080

serve-docs:
	python3 -m http.server --directory docs/build/ 9090
