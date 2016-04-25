# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSegment_inflection_point_count_01():

    pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

    assert pitch_segment.inflection_point_count == 2
