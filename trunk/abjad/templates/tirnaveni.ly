%%% Template: tirnaveni.ly
%%%
%%% Suitable for polymetric examples such as Ligeti's piano etude 'Desordre':
%%%
%%%   OFF: first-system indent, bar numbers, automatic beaming
%%%   ON:  ragged-right, forget-accidentals
%%%
%%%   * Staff and RhythmicStaff have Timing_translators, 
%%%     so each staff can have its own meter changes
%%%   * Tuplets extend full length of figures they govern
%%%   * Tuplets are always written as fraction
%%%   * Line break are allowed on spanning durations
%%%   * All breakable spanners are set to True
%%%   * Collisions are ignored
%%%   * Differently dotted note_heads are merged
%%%   * Different note_head types are merged
%%%   * Tagline is removed

\header{
   tagline = ""
}

\layout {
   indent = #0
   merge-differently-dotted = ##t
   merge-differently-headed = ##t
   ragged-right = ##t
   \context {
      \Score
      \remove Bar_number_engraver
      \remove Default_bar_line_engraver
      \remove Timing_translator
      \override Beam #'breakable = ##t
	  \override Glissando #'breakable = ##t
      \override NoteColumn #'ignore-collision = ##t
	  \override SpacingSpanner #'uniform-stretching = ##t
      \override TextScript #'staff-padding = #4
      \override TextSpanner #'breakable = ##t
      \override TupletBracket #'bracket-visibility = ##t
      \override TupletBracket #'minimum-length = #3
      \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
	  \override TupletNumber #'text = #tuplet-number::calc-fraction-text
      autoBeaming = ##f
      proportionalNotationDuration = #(ly:make-moment 1 12)
      tupletFullLength = ##t
   }

   \context {
      \Staff
      \consists Timing_translator
      \consists Default_bar_line_engraver
      \override TimeSignature #'style = #'numbered
   }

   \context {
      \RhythmicStaff
      \consists Timing_translator
      \consists Default_bar_line_engraver
      \override TimeSignature #'style = #'numbered
      \override VerticalAxisGroup #'minimum-Y-extent = #'(-2 . 4)
   }

   \context{
      \Voice
      \remove "Forbid_line_break_engraver"
    }
}
      
#(set-default-paper-size "a4")
#(set-global-staff-size 14)

\paper {
    between-system-padding = #15
    bottom-margin = 0.75\in
	left-margin = 0.75\in
	line-width = 6.75\in 
}
