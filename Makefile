#----------
# test
#----------

test:
	python setup.py test

test-all: clean
	tox

#----------
# clean
#----------

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

#----------
# publish
#----------

publish:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel --universal
	twine upload -r pypi dist/*
	rm -fr build dist .egg related.egg-info
