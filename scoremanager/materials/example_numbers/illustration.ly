% 2014-03-18 07:42

\version "2.19.3"
\language "english"

\header {}

\layout {}

\paper {}

\score {
	\new Score <<
		\new PianoStaff <<
			\context Staff = "treble" {
				\clef "treble"
				cs'8
				d'8
				ef'8
				e'8
				f'8
			}
			\context Staff = "bass" {
				\clef "bass"
				r8
				r8
				r8
				r8
				r8
			}
		>>
	>>
}