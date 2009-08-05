%%% Template: oedo.ly
%%%
%%% Suitable for online documentation.
%%%
%%%   * Tuplets extend full length of figures they govern
%%%   * Tuplets are always written as fraction
%%%   * Proportional notation is on
%%%   * Tagline is removed

\header{
   tagline = ""
}

\layout {
   indent = #0
   ragged-right = ##t

   \context { \Score
      % tuplet handling
      tupletFullLength = ##t
      \override TupletBracket #'bracket-visibility = ##t
      \override TupletBracket #'padding = #2
      % allow tuplet bracket to always be visible, even for short tuplets.
      \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
      \override TupletBracket #'minimum-length = #3
		\override TupletNumber #'text = #tuplet-number::calc-fraction-text

      proportionalNotationDuration = #(ly:make-moment 1 32)
   	\override SpacingSpanner #'strict-note-spacing = ##t  
   	\override SpacingSpanner #'strict-grace-spacing = ##t
		\override SpacingSpanner #'uniform-stretching = ##t
      \remove Bar_number_engraver
   }
}
