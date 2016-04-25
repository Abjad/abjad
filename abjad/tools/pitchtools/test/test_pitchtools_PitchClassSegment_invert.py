# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_invert_01():

    pitch_class_segment = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])

    assert pitch_class_segment.invert() == \
        pitchtools.PitchClassSegment([0, 6, 2, 8, 3, 10])
