# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___eq___01():

    range_1 = pitchtools.PitchRange.from_pitches(-39, 48)
    range_2 = pitchtools.PitchRange.from_pitches(-39, 48)

    assert range_1 == range_2
    assert not range_1 != range_2


def test_pitchtools_PitchRange___eq___02():

    range_1 = pitchtools.PitchRange.from_pitches(-39, 48)
    range_2 = pitchtools.PitchRange.from_pitches(0, 48)

    assert not range_1 == range_2
    assert range_1 != range_2
