# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_alpha_01():
    r'''Morris alpha transform of pitch-class segment.
    '''

    pitch_class_segment = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
    assert pitch_class_segment.alpha() == pitchtools.PitchClassSegment(
        [1, 7, 11, 5, 8, 3])
