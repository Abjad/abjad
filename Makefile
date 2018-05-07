.PHONY: docs build

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm -Rif
	find . -name '*egg-info' | xargs rm -Rif
	find . -name __pycache__ | xargs rm -Rif
	rm -Rif build/
	rm -Rif dist/

release:
	make clean
	make -C abjad/docs upload
	make build
	twine upload dist/abjad*.tar.gz
