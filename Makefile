.PHONY: black-check black-reformat build clean docs flake8 gh-pages isort-check \
	isort-reformat mypy pytest pytest-coverage reformat release lint test

black-check:
	black --check --diff .

black-reformat:
	black .

build:
	python -m build

clean:
	find . -name '*.pyc' -delete
	rm -rf __pycache__ .cache .tox build dist htmlcov prof source/*.egg-info

docs:
	make -C docs/ html

flake_ignore = --ignore=E203,E266,E501,W503
flake_options = --isolated --max-line-length=88

flake8:
	flake8 ${flake_ignore} ${flake_options}

gh-pages:
	rm -rf gh-pages/
	git clone --depth=1 https://github.com/Abjad/abjad.github.io.git gh-pages
	rsync -rtv --delete --exclude=.git docs/build/html/ gh-pages/
	cd gh-pages && \
		touch .nojekyll && \
		git add --all . && \
		git commit --allow-empty -m "Update docs" && \
		git push origin master
	rm -rf gh-pages/

isort-check:
	isort --case-sensitive --check-only --diff --line-width=88 --multi-line=3 \
		--project=abjad --thirdparty=ply --thirdparty=roman --thirdparty=uqbar \
		--trailing-comma --use-parentheses .

isort-reformat:
	isort --case-sensitive --line-width=88 --multi-line=3 \
		--project=abjad --thirdparty=ply --thirdparty=roman --thirdparty=uqbar \
		--trailing-comma  --use-parentheses .

mypy:
	mypy source
	mypy tests

pytest:
	pytest source tests

pytest-coverage:
	pytest --cov-config=.coveragerc --cov-report=html --cov=abjad abjad tests \
		&& rm -rf htmlcov/

reformat: black-reformat isort-reformat

release:
	make -C docs/ clean html
	make clean
	make build
	twine upload dist/*
	make gh-pages

lint: black-check flake8 isort-check mypy

test: lint pytest
