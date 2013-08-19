# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet_is_transposed_subset_01():

    small = pitchtools.NumberedPitchClassSet([9, 10, 11])
    big = pitchtools.NumberedPitchClassSet([0, 1, 2, 3])

    assert small.is_transposed_subset(big)
    assert not big.is_transposed_subset(small)


def test_NumberedPitchClassSet_is_transposed_subset_02():

    small = pitchtools.NumberedPitchClassSet([5, 7, 9])
    big = pitchtools.NumberedPitchClassSet([0, 1, 2, 3])

    assert not small.is_transposed_subset(big)
    assert not big.is_transposed_subset(small)
