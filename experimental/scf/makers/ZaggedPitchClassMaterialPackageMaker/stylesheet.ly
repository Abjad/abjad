\version "2.15.13"
\include "english.ly"
\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 14)

\layout {
	indent = #0
	ragged-right = ##t
}

\paper {
	makup-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
	system-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 10) (stretchability . 0))
}