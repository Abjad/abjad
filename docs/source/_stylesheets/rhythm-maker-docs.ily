\layout {

    \accidentalStyle forget
    indent = 0
    ragged-right = ##t

    \context {
        \name GlobalContext
        \type Engraver_group
        \consists Axis_group_engraver
        \consists Staff_collecting_engraver
        \consists Time_signature_engraver
        \override TimeSignature.X-extent = #'(0 . 0)
        \override TimeSignature.X-offset = #ly:self-alignment-interface::x-aligned-on-self
        \override TimeSignature.break-align-symbol = ##f
        \override TimeSignature.break-visibility = #end-of-line-invisible
        \override TimeSignature.font-size = 1
        \override TimeSignature.self-alignment-X = #center
    }

    \context {
        \Staff
        \remove Time_signature_engraver
    }

    \context {
        \Score
        \remove Bar_number_engraver
        \accepts GlobalContext
        \override Beam.breakable = ##t
        \override Clef.X-extent = #'(0 . 0)
        \override SpacingSpanner.strict-grace-spacing = ##t
        \override SpacingSpanner.strict-note-spacing = ##t
        \override SpacingSpanner.uniform-stretching = ##t
        \override TupletBracket.bracket-visibility = ##t
        \override TupletBracket.minimum-length = 3
        \override TupletBracket.padding = 2
        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
        \override TupletNumber.text = #tuplet-number::calc-fraction-text
        autoBeaming = ##f
        proportionalNotationDuration = #(ly:make-moment 1 24)
        tupletFullLength = ##t
    }
}
