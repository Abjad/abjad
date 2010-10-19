%%% Template: paris.ly
%%%
%%% Suitable for rhythmic examples:
%%%   OFF: first-system indent, bar numbers, automatic beaming
%%%   ON:  ragged-right, forget-accidentals
%%%
%%%   * Tuplets extend full length of figures they govern
%%%   * Tuplets are always written as fraction
%%%   * Line break are allowed on spanning durations
%%%   * All breakable spanners are set to True
%%%   * Collisions are ignored
%%%   * Paper layout is landscape

\header {
   tagline = ""
}

\layout {
   indent = #0
   ragged-right = ##t

   \context {
      \Score

      % proportional notation
      proportionalNotationDuration = #(ly:make-moment 1 64)
      %proportionalNotationDuration = #(ly:make-moment 1 74)
   	%\override SpacingSpanner #'strict-note-spacing = ##t  
   	\override SpacingSpanner #'strict-grace-spacing = ##t
		\override SpacingSpanner #'uniform-stretching = ##t

      % breakable spanners
		\override Glissando #'breakable = ##t
      \override Beam #'breakable = ##t
      \override TextSpanner #'breakable = ##t

      % collisions
      \override NoteColumn #'ignore-collision = ##t

      % beaming
      autoBeaming = ##f

      % tuplet handling
      tupletFullLength = ##t
		\override TupletNumber #'text = #tuplet-number::calc-fraction-text
      \override TupletBracket #'bracket-visibility = ##t
      \override TupletBracket #'padding = #2
      % allow tuplet bracket to always be visible, even for short tuplets.
      \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
      \override TupletBracket #'minimum-length = #3

      % bar numbers
      %\remove Bar_number_engraver

      % text handling
      \override TextScript #'staff-padding = #4

   }

   \context {
      \Staff
      \override TimeSignature #'style = #'numbered
   }

   \context {
      \RhythmicStaff
      \override TimeSignature #'style = #'numbered
      \override VerticalAxisGroup #'minimum-Y-extent = #'(-2 . 4)
   }

   \context{
      \Voice
      % allow line break in spanning durations.
      \remove "Forbid_line_break_engraver"
    }
}
      
#(set-default-paper-size "a4" 'landscape)
#(set-global-staff-size 12)

\paper {
   between-system-padding = #15
	bottom-margin = 0.75\in
	left-margin = 0.75\in
}
