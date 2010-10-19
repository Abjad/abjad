%%% Template: tangiers.ly
%%%
%%%
%%% For rhythmic sketches with no durations less than the 64th note.
%%%
%%% Suitable for sketches because first-sytem indent, bar numbers,
%%% time signatures and automatica beaming are all turned off and
%%% because ragged-right is turned on and forget-accidentals are
%%% turned on.
%%%
%%% Suitable for rhythms because tuplets extend the full length
%%% of the figures they govern.


\header {
   tagline = ""
}

\layout {
   ragged-right = ##t

   \context {
      \Score
      proportionalNotationDuration = #(ly:make-moment 1 64)
      autoBeaming = ##f
      tupletFullLength = ##t
      \override TupletBracket #'bracket-visibility = ##t
      \remove Bar_number_engraver
   }

   \context {
      \Staff
      \override TimeSignature #'stencil = ##f
   }

   \context {
      \RhythmicStaff
      \override TimeSignature #'stencil = ##f
   }
   
   indent = #0
}
      
#(set-global-staff-size 14)
