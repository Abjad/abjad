.PHONY: docs build gh-pages

black-check:
	black --check --diff .

black-reformat:
	black .

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .cache
	rm -Rif .tox
	rm -Rif __pycache__
	rm -Rif build
	rm -Rif dist
	rm -Rif htmlcov
	rm -Rif prof

docs:
	make -C docs/ html

flake_ignore = --ignore=E203,E266,E501,W503
flake_options = --isolated --max-line-length=88

flake8:
	flake8 ${flake_ignore} ${flake_options}

gh-pages:
	rm -Rf gh-pages/
	git clone https://github.com/Abjad/abjad.github.io.git gh-pages
	rsync -rtv --del --exclude=.git docs/build/html/ gh-pages/
	cd gh-pages && \
		touch .nojekyll && \
		git add --all . && \
		git commit --allow-empty -m "Update docs" && \
		git push -u origin master
	rm -Rf gh-pages/

isort-check:
	isort \
	--case-sensitive \
	--check-only \
	--diff \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--project=abjadext \
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

isort-reformat:
	isort \
	--case-sensitive \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--project=abjadext \
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

jupyter-test:
	jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True tests/test.ipynb

mypy:
	mypy abjad
	mypy tests

project = abjad

pytest:
	pytest abjad tests

pytest-coverage:
	rm -Rf htmlcov/
	pytest \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov=${project} \
	abjad tests

pytest-x:
	pytest -x abjad tests

reformat:
	make black-reformat
	make isort-reformat

release:
	make -C docs/ clean html
	make clean
	make build
	twine upload dist/*.tar.gz
	make gh-pages

check:
	make black-check
	make flake8
	make isort-check
	make mypy

test:
	make black-check
	make flake8
	make isort-check
	make mypy
	make pytest
