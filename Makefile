.PHONY: docs build

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm -Rif
	find . -name '*egg-info' | xargs rm -Rif
	find . -name '.*_cache' | xargs rm -Rif
	find . -name .coverage | xargs rm -Rif
	find . -name __pycache__ | xargs rm -Rif
	rm -Rif build/
	rm -Rif dist/

docs:
	make -C docs html

release:
	make clean
	make docs
	make build
	make -C abjad/docs upload
	twine upload dist/*.tar.gz
