# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment___add___01():
    r'''Adding pitch-class segments returns a new pitch-class segment.
    '''

    pitch_class_segment_1 = pitchtools.PitchClassSegment([0, 1, 2])
    pitch_class_segment_2 = pitchtools.PitchClassSegment([3, 4, 5])

    assert pitch_class_segment_1 + pitch_class_segment_2 == \
        pitchtools.PitchClassSegment([0, 1, 2, 3, 4, 5])
