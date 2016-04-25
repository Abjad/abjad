# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSet_issubset_01():

    pitch_set_1 = pitchtools.PitchSet([-1, 3, 4])
    pitch_set_2 = pitchtools.PitchSet(range(-5, 5))

    assert pitch_set_1.issubset(pitch_set_2)
    assert not pitch_set_2.issubset(pitch_set_1)


def test_pitchtools_PitchSet_issubset_02():

    pitch_set_1 = pitchtools.PitchSet([0, 1, 2])
    pitch_set_2 = pitchtools.PitchSet([0, 1, 2])

    assert pitch_set_1.issubset(pitch_set_2)
    assert pitch_set_2.issubset(pitch_set_1)
