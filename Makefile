clean:
	rm -Rif Abjad.egg-info/
	rm -Rif build/
	rm -Rif dist/

release:
	make -C abjad/docs upload
	python setup.py sdist
	twine upload dist/*
