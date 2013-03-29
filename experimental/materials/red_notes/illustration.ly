% Abjad revision 5047M
% 2012-02-13 16:15

\version "2.15.24"
\include "english.ly"
\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

\include "/Users/trevorbaca/Documents/baca/scf/stylesheets/clean_letter_14.ly"

\header {
	tagline = \markup { "" }
	title = \markup { red notes }
}

\score {
	\new Score <<
		\new PianoStaff <<
			\context Staff = "treble" {
				\clef "treble"
				d'16
				e'8
				f'16
				d'8
				e'16
				f'8
				d'16
				e'8
				f'16
				d'8
				e'16
				f'8
				d'16
				e'8
				f'16
				d'8
				e'16
				f'8
				r4
			}
			\context Staff = "bass" {
				\clef "bass"
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r4
			}
		>>
	>>
}
