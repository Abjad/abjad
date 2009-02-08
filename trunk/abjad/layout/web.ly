\layout {
   \context { \Score
      \override TupletBracket #'bracket-visibility = ##t
      \override TupletBracket #'padding = #2
      proportionalNotationDuration = #(ly:make-moment 1 32)
   	\override SpacingSpanner #'strict-note-spacing = ##t  
   	\override SpacingSpanner #'strict-grace-spacing = ##t
		\override SpacingSpanner #'uniform-stretching = ##t
      \remove Bar_number_engraver
   }
   indent = #0
}
