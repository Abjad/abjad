.PHONY: docs build gh-pages

black-check:
	black --check --diff --exclude='.*boilerplate.*' --target-version=py38 .

black-reformat:
	black --exclude='.*boilerplate.*' --target-version=py38 .

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/

docs:
	make -C docs/ html

flake_exclude = --exclude=boilerplate,abjad/__init__.py
flake_ignore = --ignore=E203,E266,E501,W503
flake_options = --isolated --max-line-length=88

flake8:
	flake8 ${flake_exclude} ${flake_ignore} ${flake_options}

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
	--recursive \
	--skip=abjad/__init__.py \
	--skip-glob='*boilerplate*' \
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

isort-reformat:
	isort \
	--apply \
	--case-sensitive \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--project=abjadext \
	--recursive \
	--skip=abjad/__init__.py \
	--skip-glob='*boilerplate*' \
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

jupyter-test:
	jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True tests/test.ipynb

mypy:
	mypy .

project = abjad

pytest:
	rm -Rf htmlcov/
	pytest \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov-report=term \
	--cov=${project}/ \
	--durations=20 \
	.

pytest-x:
	rm -Rf htmlcov/
	pytest \
	-x \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov-report=term \
	--cov=${project}/ \
	--durations=20 \
	.

reformat:
	make black-reformat
	make isort-reformat

release:
	make -C docs/ clean html
	make clean
	make build
	pip install -U twine
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
