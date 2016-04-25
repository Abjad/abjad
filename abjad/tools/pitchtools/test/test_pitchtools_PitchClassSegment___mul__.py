# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment___mul___01():

    pitch_class_segment_1 = pitchtools.PitchClassSegment([0, 1, 11, 9])
    pitch_class_segment_2 = pitch_class_segment_1 * 2

    assert pitch_class_segment_2 == \
        pitchtools.PitchClassSegment([0, 1, 11, 9, 0, 1, 11, 9])
