all:
	lilypond -dno-print-pages contexts.ly > ../abjad/lyscrape.py
	echo "" >> ../abjad/lyscrape.py
	lilypond -dno-print-pages current_module.ly >> ../abjad/lyscrape.py
	echo "" >> ../abjad/lyscrape.py
	lilypond -dno-print-pages engravers.ly >> ../abjad/lyscrape.py
	echo "" >> ../abjad/lyscrape.py
	lilypond -dno-print-pages grob_interfaces.ly >> ../abjad/lyscrape.py
	echo "" >> ../abjad/lyscrape.py
	lilypond -dno-print-pages interface_properties.ly >> ../abjad/lyscrape.py
	echo "" >> ../abjad/lyscrape.py
	lilypond -dno-print-pages language_pitch_names.ly >> ../abjad/lyscrape.py
	echo "" >> ../abjad/lyscrape.py
	# lilypond -dno-print-pages markup_functions.ly >> ../abjad/lyscrape.py
	# echo "" >> ../abjad/lyscrape.py
	lilypond -dno-print-pages music_glyphs.ly >> ../abjad/lyscrape.py
	black --target-version=py38 ../abjad/lyscrape.py
