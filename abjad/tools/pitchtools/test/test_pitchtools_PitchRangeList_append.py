# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRangeList_append_01():

    pitch_ranges_1 = pitchtools.PitchRangeList(['[A0, C8]'])
    pitch_ranges_1.append('[C3, F#5]')
    pitch_ranges_2 = pitchtools.PitchRangeList(['[A0, C8]', '[C3, F#5]'])

    assert pitch_ranges_1 == pitch_ranges_2
