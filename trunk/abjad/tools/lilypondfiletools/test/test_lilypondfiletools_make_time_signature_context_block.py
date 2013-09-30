# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_make_time_signature_context_block_01():

    context_block = lilypondfiletools.make_time_signature_context_block()

    assert testtools.compare(
        context_block,
        r'''
        \context {
            \name TimeSignatureContext
            \type Engraver_group
            \consists Axis_group_engraver
            \consists Time_signature_engraver
            \override TimeSignature #'X-extent = #'(0 . 0)
            \override TimeSignature #'X-offset = #ly:self-alignment-interface::x-aligned-on-self
            \override TimeSignature #'Y-extent = #'(0 . 0)
            \override TimeSignature #'break-align-symbol = ##f
            \override TimeSignature #'break-visibility = #end-of-line-invisible
            \override TimeSignature #'font-size = #3
            \override TimeSignature #'self-alignment-X = #center
            \override VerticalAxisGroup #'default-staff-staff-spacing = #'((basic-distance . 0) (minimum-distance . 12) (padding . 4) (stretchability . 0))
        }
        '''
        )
