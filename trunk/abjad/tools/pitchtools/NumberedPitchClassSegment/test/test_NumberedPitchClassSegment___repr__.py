# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NumberedPitchClassSegment


def test_NumberedPitchClassSegment___repr___01():
    r'''Numbered chromatic pitch-class segment repr is evaluable.
    '''

    cpns = [-2, -1.5, 6, 7, -1.5, 7]
    numbered_chromatic_pitch_class_segment_1 = pitchtools.NumberedPitchClassSegment(cpns)
    numbered_chromatic_pitch_class_segment_2 = eval(repr(numbered_chromatic_pitch_class_segment_1))

    assert isinstance(numbered_chromatic_pitch_class_segment_1, NumberedPitchClassSegment)
    assert isinstance(numbered_chromatic_pitch_class_segment_2, NumberedPitchClassSegment)
