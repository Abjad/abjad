# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import PitchRange


def test_pitchtools_PitchRangeList___repr___01():

    pitch_ranges_1 = pitchtools.PitchRangeList(['[A0, C8]', '[C3, F#5]'])
    pitch_ranges_2 = pitchtools.PitchRangeList(pitch_ranges_1)

    assert pitch_ranges_1 == pitch_ranges_2
