% 2014-06-30 10:24

\version "2.19.8"
\language "english"

\header {
	tagline = \markup {}
}

\layout {
	indent = #0
	ragged-right = ##t
}

\score {
	\new Score \with {
		\override BarLine #'transparent = ##t
		\override BarNumber #'stencil = ##f
		\override Clef #'stencil = ##f
		\override NoteHead #'no-ledgers = ##t
		\override NoteHead #'transparent = ##t
		\override StaffSymbol #'transparent = ##t
		\override Stem #'transparent = ##t
		\override TimeSignature #'stencil = ##f
	} <<
		\new Staff {
			\time 2/4
			\break
			c'2
			\tempo 8=72
			\break
			c'2
			\tempo 8=108
			\break
			c'2
			\tempo 8=90
			\break
			c'2
			\tempo 8=135
			\break
			c'2
		}
	>>
}