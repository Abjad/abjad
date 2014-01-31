\layout {
    \context {
        \type Engraver_group
        \name TimeSignatureContext
        \consists Axis_group_engraver
        \consists Bar_number_engraver
        \consists Mark_engraver
        \consists Metronome_mark_engraver
        \consists Text_engraver
        \consists Time_signature_engraver
        \override BarNumber.X-extent = #'(0 . 0)
        \override BarNumber.Y-extent = #'(0 . 0)
        \override BarNumber.extra-offset = #'(-8 . -2)
        \override BarNumber.font-size = 1
        \override BarNumber.stencil = #(make-stencil-circler 0.1 0.7 ly:text-interface::print)
        \override MetronomeMark.X-extent = #'(0 . 0)
        \override MetronomeMark.X-offset = #ly:self-alignment-interface::x-aligned-on-self
        \override MetronomeMark.break-align-symbols = #'(time-signature)
        \override MetronomeMark.extra-offset = #'(3 . -5.5)
        \override MetronomeMark.font-size = 3
        \override RehearsalMark.X-extent = #'(0 . 0)
        \override RehearsalMark.break-align-symbols = #'(time-signature)
        \override RehearsalMark.break-visibility = #end-of-line-invisible
        \override RehearsalMark.extra-offset = #'(-1 . 0)
        \override RehearsalMark.font-size = 10
        \override RehearsalMark.self-alignment-X = #CENTER
        \override TextScript.padding = 8
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
        \remove Bar_number_engraver
        \remove Mark_engraver
        \remove Metronome_mark_engraver
    }
}
