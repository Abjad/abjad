%%% Template: tirnaveni.ly
%%%
%%% Suitable for poly-metric examples such as Ligeti's piano etude 'Desordre':
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
   ragged-right = ##t

   merge-differently-dotted = ##t
   merge-differently-headed = ##t

   \context {
      \Score

      % proportional notation
      proportionalNotationDuration = #(ly:make-moment 1 12)
   	%\override SpacingSpanner #'strict-note-spacing = ##t  
   	%\override SpacingSpanner #'strict-grace-spacing = ##t
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
      % allow tuplet bracket to always be visible, even for short tuplets.
      \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
      \override TupletBracket #'minimum-length = #3

      % bar numbers
      \remove Bar_number_engraver

      % bar lines
      \remove Default_bar_line_engraver
      
      % timing administration
      \remove Timing_translator
      
      % markup overrides
      \override TextScript #'staff-padding = #4
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
      % allow line break in spanning durations.
      \remove "Forbid_line_break_engraver"
    }
}
      
%#(set-default-paper-size "a4" 'landscape)
#(set-default-paper-size "a4")
#(set-global-staff-size 14)

\paper {
   between-system-padding = #15
	bottom-margin = 0.75\in
	left-margin = 0.75\in
	line-width = 6.75\in 
}
