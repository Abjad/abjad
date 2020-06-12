MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
SCORE_NAME := $(lastword $(subst /, ,$(firstword $(subst build, ,$(MAKEFILE_PATH)))))
BUILD_TARGET := $(notdir $(patsubst %/,%,$(dir $(MAKEFILE_PATH))))
BUILD_PREFIX := $(SCORE_NAME)-$(BUILD_TARGET)

all:
	make front-cover
	make preface
	make music
	make back-cover
	make score
	make parts
	make clean

front-cover:
	xelatex front-cover.tex
	xelatex front-cover.tex

back-cover:
	xelatex back-cover.tex
	xelatex back-cover.tex

preface:
	xelatex preface.tex
	xelatex preface.tex

music:
	lilypond music.ly

parts:
	lilypond parts.ly

score:
	xelatex score.tex
	xelatex score.tex

clean:
	rm -f *.log
	rm -f *.aux

dist:
	mkdir -p ../../distribution/$(BUILD_PREFIX)
	cp score.pdf ../../distribution/$(BUILD_PREFIX)/$(BUILD_PREFIX)-score.pdf
	for part in parts-*.pdf; do \
		mv $$part ../../distribution/$(BUILD_PREFIX)/$(BUILD_PREFIX)-$$part; \
	done;
	cd ../../distribution && zip -r $(BUILD_PREFIX).zip $(BUILD_PREFIX) 

help:
	@echo ""
	@echo "make (all)           - compile score and parts PDFs"
	@echo "                       copy score and parts PDFs to distribution/"
	@echo "                       create ZIP archive of score and parts"
	@echo "                       clean extraneous LaTeX files"
	@echo "make front-cover     - compile front-cover PDF"
	@echo "make preface         - compile preface PDF"
	@echo "make music           - compile music PDF"
	@echo "make back-cover      - compile back-cover PDF"
	@echo "make score           - compile score PDF"
	@echo "make parts           - compile parts PDFs"
	@echo "make dist            - copy score and parts PDFs to distribution/"
	@echo "                       create ZIP archive of score and parts"
	@echo "make clean           - clean extraneous LaTeX files"
	@echo "make help            - print this message"
	@echo ""
