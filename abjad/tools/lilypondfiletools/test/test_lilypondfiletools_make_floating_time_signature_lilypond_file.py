# -*- coding: utf-8 -*-
import abjad


def test_lilypondfiletools_make_floating_time_signature_lilypond_file_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    lilypond_file = \
        abjad.make_floating_time_signature_lilypond_file(staff)
    context_block = lilypond_file.layout_block.items[1]

    assert format(context_block) == abjad.String.normalize(
        r'''
        \context {
            \name TimeSignatureContext
            \type Engraver_group
            \consists Axis_group_engraver
            \consists Time_signature_engraver
            \override TimeSignature.X-extent = #'(0 . 0)
            \override TimeSignature.X-offset = #ly:self-alignment-interface::x-aligned-on-self
            \override TimeSignature.Y-extent = #'(0 . 0)
            \override TimeSignature.break-align-symbol = ##f
            \override TimeSignature.break-visibility = #end-of-line-invisible
            \override TimeSignature.font-size = #1
            \override TimeSignature.self-alignment-X = #center
            \override VerticalAxisGroup.default-staff-staff-spacing = #'((basic-distance . 0) (minimum-distance . 10) (padding . 6) (stretchability . 0))
        }
        '''
        )
