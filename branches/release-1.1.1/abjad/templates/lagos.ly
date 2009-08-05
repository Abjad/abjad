%%% Template: lagos.ly
%%%
%%% Compact, non-proportional rhythmic notation.
%%%
%%%
%%%   * Tuplets extend full length of figures they govern
%%%   * Tuplets are always written as fraction
%%%   * Proportional notation is OFF
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

      \remove Bar_number_engraver
   }
}

#(set-global-staff-size 15)
