all:
	make clean
	make book
	make latex

book:
	ajv book \
	    source.tex \
		-a ./assets \
		-g ./abjadbook.cfg \
		-y ./stylesheet.ily \
		-o target.tex

clean:
	rm -Rif assets
	rm -Rif target.*

latex:
	pdflatex --shell-escape target.tex