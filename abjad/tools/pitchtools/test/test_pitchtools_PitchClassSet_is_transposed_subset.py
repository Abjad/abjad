# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet_is_transposed_subset_01():

    small = pitchtools.PitchClassSet([9, 10, 11])
    big = pitchtools.PitchClassSet([0, 1, 2, 3])

    assert small.is_transposed_subset(big)
    assert not big.is_transposed_subset(small)


def test_pitchtools_PitchClassSet_is_transposed_subset_02():

    small = pitchtools.PitchClassSet([5, 7, 9])
    big = pitchtools.PitchClassSet([0, 1, 2, 3])

    assert not small.is_transposed_subset(big)
    assert not big.is_transposed_subset(small)
