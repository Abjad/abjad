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
        \type Engraver_group
        \name TimeSignatureContext
        \consists Time_signature_engraver
        \consists Axis_group_engraver
        \override TimeSignature.X-extent = #'(0 . 0)
        \override TimeSignature.X-offset = #ly:self-alignment-interface::x-aligned-on-self
        \override TimeSignature.Y-extent = #'(0 . 0)
        \override TimeSignature.break-align-symbol = ##f
        \override TimeSignature.break-visibility = #end-of-line-invisible
        \override TimeSignature.font-size = 2
        \override TimeSignature.self-alignment-X = #center
        \override VerticalAxisGroup.default-staff-staff-spacing = #'(
            (basic-distance . 0)
            (minimum-distance . 12)
            (padding . 0)
            (stretchability . 0)
            )
    }
    \context {
        \Score
        \accepts TimeSignatureContext
        \override BarLine.hair-thickness = 0.5
        \override BarNumber.stencil = ##f
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
        \override TextScript.Y-extent = #'(-1.5 . 1.5)
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
    left-margin = 12
    markup-markup-spacing #'basic-distance = 16
    markup-system-spacing #'basic-distance = 34
    oddFooterMarkup = \markup {}
    oddHeaderMarkup = \markup {}
    %score-markup-spacing #'minimum-distance = 20
    score-system-spacing #'minimum-distance = 28
    top-markup-spacing #'minimum-distance = 6
}

