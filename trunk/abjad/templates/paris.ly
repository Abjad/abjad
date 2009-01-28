%%% Template: paris.ly
%%%
%%%
%%% Suitable for rhythmic examples because 
%%% first-sytem indent, bar numbers, automatica beaming are all turned off and
%%% because ragged-right is turned on and forget-accidentals are turned on.
%%%
%%% Suitable for rhythms because tuplets extend the full length
%%% of the figures they govern.
%%% Tuplets are always written as fraction.
%%% Staff and RhythmicStaff have Timing_translators, so each staff can have
%%% its own meter changes.
%%%
%%% Line break are allowed on spanning durations.
%%% All breakable spanners are set to True.
%%% Collisions are ignored.


\layout {
   indent = #0
   ragged-right = ##t

   \context {
      \Score
      %%% proportional notation
      %proportionalNotationDuration = #(ly:make-moment 1 64)
      proportionalNotationDuration = #(ly:make-moment 1 74)
   	\override SpacingSpanner #'strict-note-spacing = ##t  
   	\override SpacingSpanner #'strict-grace-spacing = ##t
		\override SpacingSpanner #'uniform-stretching = ##t

      %%% breakable spanners
		\override Glissando #'breakable = ##t
      \override Beam #'breakable = ##t
      \override TextSpanner #'breakable = ##t
      %%% collisions
      \override NoteColumn #'ignore-collision = ##t

      autoBeaming = ##f
      tupletFullLength = ##t
      \override TupletBracket #'bracket-visibility = ##t
		\override TupletNumber #'text = #tuplet-number::calc-fraction-text

      \remove Bar_number_engraver
      
      \remove Timing_translator
      \remove Default_bar_line_engraver
   }

   \context {
      \Staff
      %\override TimeSignature #'stencil = ##f
      \consists Timing_translator
      \consists Default_bar_line_engraver
   }

   \context {
      \RhythmicStaff
      \consists Timing_translator
      \consists Default_bar_line_engraver
      \override VerticalAxisGroup #'minimum-Y-extent = #'(-4 . 2)
   }

   \context{ \Voice
      %%% allow line break in spanning durations.
      \remove "Forbid_line_break_engraver"
    }
}
      
#(set-default-paper-size "a4" 'landscape)
%#(set-default-paper-size "a4")
#(set-global-staff-size 14)
