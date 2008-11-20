\layout {
   \context { \Score
      \override TupletBracket #'bracket-visibility = ##t
      \override TupletBracket #'padding = #2
      proportionalNotationDuration = #(ly:make-moment 1 32)
      \remove Bar_number_engraver
   }
   indent = #0
}
