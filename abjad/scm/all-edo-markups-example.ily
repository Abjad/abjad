\version "2.25.16"
#(set-default-paper-size "letterportrait")
#(set-global-staff-size 15)

\header {tagline = ##f}

\paper {
  system-system-spacing = #'((basic-distance . 30) (minimum-distance . 30) (padding . 6))
}

\layout {
	indent = #1
	ragged-last = ##t
    ragged-right = ##t
	\override Beam.stencil = ##f
	\override Staff.BarLine.stencil = ##f
	\override Flag.stencil = ##f
	\override Staff.TimeSignature.stencil = ##f
	\override SpacingSpanner.strict-grace-spacing = ##t
	\override SpacingSpanner.uniform-stretching = ##t
	\override SpacingSpanner.strict-note-spacing = ##t
    \override SpacingSpanner.uniform-stretching = ##t
\context {
	\Score
	proportionalNotationDuration = \musicLength 1*1/30
	barNumberVisibility = ##f
}
}
