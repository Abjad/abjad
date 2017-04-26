# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRangeList___contains___01():

    pitch_ranges = pitchtools.PitchRangeList(['[C3, C6]', '[C4, C6]'])

    assert '[C3, C6]' in pitch_ranges
    assert (-12, 24) in pitch_ranges
    assert (-39, 48) not in pitch_ranges
