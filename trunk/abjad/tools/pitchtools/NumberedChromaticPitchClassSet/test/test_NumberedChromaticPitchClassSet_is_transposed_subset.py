from abjad import *


def test_NumberedChromaticPitchClassSet_is_transposed_subset_01():

    small = pitchtools.NumberedChromaticPitchClassSet([9, 10, 11])
    big = pitchtools.NumberedChromaticPitchClassSet([0, 1, 2, 3])

    assert small.is_transposed_subset(big)
    assert not big.is_transposed_subset(small)


def test_NumberedChromaticPitchClassSet_is_transposed_subset_02():

    small = pitchtools.NumberedChromaticPitchClassSet([5, 7, 9])
    big = pitchtools.NumberedChromaticPitchClassSet([0, 1, 2, 3])

    assert not small.is_transposed_subset(big)
    assert not big.is_transposed_subset(small)
