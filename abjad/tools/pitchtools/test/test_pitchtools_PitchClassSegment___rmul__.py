# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment___rmul___01():

    pitch_class_segment_1 = pitchtools.PitchClassSegment([0, 1, 11, 9])
    pitch_class_segment_2 = 2 * pitch_class_segment_1

    assert pitch_class_segment_2 == \
        pitchtools.PitchClassSegment([0, 1, 11, 9, 0, 1, 11, 9])
