\include "../../../stylesheets/time-signature-context.ily"

#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 10)

\layout {
    \accidentalStyle forget
    indent = 0
    ragged-bottom = ##t
    ragged-last = ##t
    ragged-right = ##t
    \context {
        \Voice
        \consists Horizontal_bracket_engraver
        \remove Forbid_line_break_engraver
    }
    \context {
        \Staff
        \remove Time_signature_engraver
    }
    \context {
        \RhythmicStaff
        \remove Time_signature_engraver
        \override BarLine.bar-extent = #'(-2 . 4)
        \override Beam.positions = #'(4 . 4)
        \override Stem.length = 8
    }
    \context {
        \Score
        \accepts TimeSignatureContext
        \override BarLine.hair-thickness = 0.5
        \override BarNumber.color = #red
        \override BarNumber.transparent = ##t
        \override Beam.breakable = ##t
        \override DynamicLineSpanner.Y-extent = #'(-1.5 . 1.5)
        \override Glissando.breakable = ##t
        \override MetronomeMark.extra-offset = #'(3 . -3)
        \override MetronomeMark.font-size = 3
        \override NoteCollision.merge-differently-dotted = ##t
        \override NoteColumn.ignore-collision = ##t
        \override SpacingSpanner.strict-grace-spacing = ##t
        \override SpacingSpanner.strict-note-spacing = ##t
        \override SpacingSpanner.uniform-stretching = ##t
        \override SpanBarStub.color = #green
        \override StaffGrouper.staffgroup-staff-spacing = #'(
            (basic-distance . 10.5)
            (minimum-distance . 10)
            (padding . 1)
            (stretchability . 9)
            )
        \override Stem.direction = #up
        \override StemTremolo.beam-width = 1.5
        \override StemTremolo.flag-count = 4
        \override StemTremolo.slope = 0.5
        \override StemTremolo.Y-offset = -4
        \override TupletBracket.breakable = ##t
        \override TupletBracket.direction = #up
        \override TupletBracket.full-length-to-extent = ##f
        \override TupletBracket.padding = 2.0
        \override TupletNumber.font-size = 1
        \override TupletNumber.text = #tuplet-number::calc-fraction-text
        autoBeaming = ##f
        proportionalNotationDuration = #(ly:make-moment 1 64)
        tupletFullLength = ##t
    }
}

\paper {
    evenFooterMarkup = \markup {}
    evenHeaderMarkup = \markup {}
    left-margin = 14
    markup-system-spacing #'minimum-distance = 36
    oddFooterMarkup = \markup {}
    oddHeaderMarkup = \markup {}
    print-all-headers = ##t
    score-system-spacing #'minimum-distance = 12
    top-markup-spacing #'minimum-distance = 6
}
