# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet_invert_01():

    assert pitchtools.PitchClassSet([0, 1, 5]).invert() == \
        pitchtools.PitchClassSet([0, 7, 11])
    assert pitchtools.PitchClassSet([1, 2, 6]).invert() == \
        pitchtools.PitchClassSet([6, 10, 11])
