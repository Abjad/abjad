.PHONY: docs build

codePath = abjad
errors = E123,E203,E265,E266,E501,W503
origin := $(shell git config --get remote.origin.url)
paths = ${codePath}/ tests/ *.py

black-check:
	black --target-version py36 --exclude '.*boilerplate.*' --check --diff ${paths}

black-reformat:
	black --target-version py36 --exclude '.*boilerplate.*' ${paths}

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif .cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif prof/
	rm -Rif *.egg-info/

docs:
	make -C docs/ html

flake8:
	flake8 --max-line-length=90 --isolated --ignore=${errors} ${paths}

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
		--multi-line 1 \
		--recursive \
		--skip-glob '*boilerplate*' \
		--trailing-comma \
		--use-parentheses -y \
		${paths}

mypy:
	mypy --ignore-missing-imports ${codePath}/

pytest:
	rm -Rf htmlcov/
	pytest \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${codePath}/ \
		--cov=tests/

pytest-x:
	rm -Rf htmlcov/
	pytest \
		-x \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${codePath}/ \
		--cov=tests/

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
