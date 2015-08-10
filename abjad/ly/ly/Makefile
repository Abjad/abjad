# Makefile

all: contexts current_module engravers grob_interfaces interface_properties language_pitch_names markup_functions music_glyphs

contexts: contexts.ly
	lilypond -dno-print-pages contexts.ly > ../contexts.py

current_module: current_module.ly
	lilypond -dno-print-pages current_module.ly > ../current_module.py

engravers: engravers.ly
	lilypond -dno-print-pages engravers.ly > ../engravers.py

grob_interfaces: grob_interfaces.ly
	lilypond -dno-print-pages grob_interfaces.ly > ../grob_interfaces.py

interface_properties: interface_properties.ly
	lilypond -dno-print-pages interface_properties.ly > ../interface_properties.py

language_pitch_names: language_pitch_names.ly
	lilypond -dno-print-pages language_pitch_names.ly > ../language_pitch_names.py

markup_functions: markup_functions.ly
	lilypond -dno-print-pages markup_functions.ly > ../markup_functions.py

music_glyphs: music_glyphs.ly
	lilypond -dno-print-pages music_glyphs.ly > ../music_glyphs.py