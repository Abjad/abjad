.PHONY: docs build

project = abjad
errors = E123,E203,E265,E266,E501,W503
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

black-check:
	black --target-version py36 --exclude '.*boilerplate.*' --check --diff ${formatPaths}

black-reformat:
	black --target-version py36 --exclude '.*boilerplate.*' ${formatPaths}

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
	flake8 --max-line-length=90 --isolated --ignore=${errors} ${formatPaths}

gh-pages:
	rm -Rf gh-pages/
	git clone $(origin) gh-pages/
	cd gh-pages/ && \
		git checkout gh-pages || git checkout --orphan gh-pages
	rsync -rtv --del --exclude=.git docs/build/html/ gh-pages/
	cd gh-pages && \
		touch .nojekyll && \
		git add --all . && \
		git commit --allow-empty -m "Update docs" && \
		git push -u origin gh-pages
	rm -Rf gh-pages/

isort:
	isort \
		--case-sensitive \
		--multi-line 3 \
		--project abjad \
		--project abjadext \
		--recursive \
		--skip ${project}/__init__.py \
		--skip-glob '*boilerplate*' \
		--thirdparty ply \
		--thirdparty roman \
		--thirdparty uqbar \
		--trailing-comma \
		--use-parentheses -y \
		${formatPaths}

jupyter-test:
	jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True tests/test.ipynb

mypy:
	mypy --ignore-missing-imports ${project}/

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
	make isort
	make black-reformat

release:
	make docs
	make clean
	make build
	twine upload dist/*.tar.gz
	make gh-pages

test:
	make black-check
	make flake8
	make mypy
	make pytest
