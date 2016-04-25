# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_multiply_01():

    pitch_class_segment = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])

    assert pitch_class_segment.multiply(0) == \
        pitchtools.PitchClassSegment([0, 0, 0, 0, 0, 0])
    assert pitch_class_segment.multiply(1) == \
        pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
    assert pitch_class_segment.multiply(5) == \
        pitchtools.PitchClassSegment([0, 6, 2, 8, 9, 10])
    assert pitch_class_segment.multiply(7) == \
        pitchtools.PitchClassSegment([0, 6, 10, 4, 3, 2])
