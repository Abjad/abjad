.PHONY: docs build gh-pages

project = abjad
errors = E203,E266,E501,W503
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/
flakeOptions = --exclude=boilerplate,abjad/__init__.py --isolated --max-line-length=88

black-check:
	black --target-version py38 --exclude '.*boilerplate.*' --check --diff ${formatPaths}

black-reformat:
	black --target-version py38 --exclude '.*boilerplate.*' ${formatPaths}

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

flake8:
	flake8 ${flakeOptions} --ignore=${errors} ${formatPaths}

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
		--apply \
		--case-sensitive \
		--check-only \
		--diff \
		--line-width=88 \
		--multi-line=3 \
		--project=abjad \
		--project=abjadext \
		--recursive \
		--skip=${project}/__init__.py \
		--skip-glob='*boilerplate*' \
		--thirdparty=ply \
		--thirdparty=roman \
		--thirdparty=uqbar \
		--trailing-comma \
		--use-parentheses \
		${formatPaths}

isort-reformat:
	isort \
		--case-sensitive \
		--line-width=88 \
		--multi-line=3 \
		--project=abjad \
		--project=abjadext \
		--recursive \
		--skip=${project}/__init__.py \
		--skip-glob='*boilerplate*' \
		--thirdparty=ply \
		--thirdparty=roman \
		--thirdparty=uqbar \
		--trailing-comma \
		--use-parentheses \
		${formatPaths}

jupyter-test:
	jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True tests/test.ipynb

mypy:
	mypy ${project}/

pytest:
	rm -Rf htmlcov/
	pytest \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${project}/ \
		--durations=20 \
		${testPaths}

pytest-x:
	rm -Rf htmlcov/
	pytest \
		-x \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${project}/ \
		--durations=20 \
		${testPaths}

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
	make flake8-check
	make isort-check

test:
	make black-check
	make flake8
	make isort-check
	make mypy
	make pytest
