LilyPond files
==============

Making LilyPond files
---------------------

Make a basic LilyPond input file with the ``lilyfiletools`` package:

::

	abjad> staff = Staff("c'8 d'8 e'8 f'8")
	abjad> lilypond_file = lilyfiletools.make_basic_lilypond_file(staff)


::

    abjad> lilypond_file
    LilyPondFile(Staff{4})

Inspecting file output
----------------------

LilyPond input files that you create this way come equipped with many attributes
that appear in file output:

::

	abjad> f(lilypond_file)
	% Abjad revision 4746
	% 2011-09-04 17:36
	
	\version "2.15.9"
	\include "english.ly"
	\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"
	
	\score {
		\new Staff {
			c'8
			d'8
			e'8
			f'8
		}
	}


Setting default paper size
--------------------------

Set default LilyPond paper size like this:

::

	abjad> lilypond_file.default_paper_size = '11x17', 'landscape'


::

	abjad> f(lilypond_file)
	% Abjad revision 4746
	% 2011-09-04 17:36
	
	\version "2.15.9"
	\include "english.ly"
	\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"
	
	#(set-default-paper-size "11x17" 'landscape)
	
	\score {
		\new Staff {
			c'8
			d'8
			e'8
			f'8
		}
	}


Setting global staff size
-------------------------

Set global staff size like this:

::

	abjad> lilypond_file.global_staff_size = 16


::

	abjad> f(lilypond_file)
	% Abjad revision 4746
	% 2011-09-04 17:36
	
	\version "2.15.9"
	\include "english.ly"
	\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"
	
	#(set-default-paper-size "11x17" 'landscape)
	#(set-global-staff-size 16)
	
	\score {
		\new Staff {
			c'8
			d'8
			e'8
			f'8
		}
	}
