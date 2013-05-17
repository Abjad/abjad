% Abjad revision 5333
% 2012-03-18 22:47

\version "2.15.27"
\include "english.ly"
\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

\header {
	tagline = \markup { "" }
}

\paper {
	top-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 6) (stretchability . 0))
}

\score {
	\new Score \with {
		\override BarLine #'transparent = ##t
		\override Clef #'transparent = ##t
		\override NoteHead #'transparent = ##t
		\override SpanBar #'transparent = ##t
		\override StaffSymbol #'transparent = ##t
		\override Stem #'transparent = ##t
		\override TimeSignature #'stencil = ##f
		proportionalNotationDuration = #(ly:make-moment 1 24)
	} <<
		\new RhythmicStaff {
			c'4 - \markup { \bold { staccatissimo luminoso } }
			c'4 - \markup { \italic { serenamente } }
		}
	>>
}