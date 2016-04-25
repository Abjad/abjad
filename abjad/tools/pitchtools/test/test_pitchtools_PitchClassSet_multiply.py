# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet_multiply_01():

    assert pitchtools.PitchClassSet([0, 1, 5]).multiply(5) == \
        pitchtools.PitchClassSet([0, 1, 5])
    assert pitchtools.PitchClassSet([1, 2, 6]).multiply(5) == \
        pitchtools.PitchClassSet([5, 6, 10])
    assert pitchtools.PitchClassSet([2, 3, 7]).multiply(5) == \
        pitchtools.PitchClassSet([3, 10, 11])
