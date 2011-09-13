from abjad import *


def test_NumberedChromaticPitchClassSet_transpose_01():

    pcset = pitchtools.NumberedChromaticPitchClassSet([1, 2, 5])
    assert pcset.transpose(0) == pitchtools.NumberedChromaticPitchClassSet([1, 2, 5])
    assert pcset.transpose(1) == pitchtools.NumberedChromaticPitchClassSet([2, 3, 6])
    assert pcset.transpose(2) == pitchtools.NumberedChromaticPitchClassSet([3, 4, 7])
    assert pcset.transpose(3) == pitchtools.NumberedChromaticPitchClassSet([4, 5, 8])
    assert pcset.transpose(4) == pitchtools.NumberedChromaticPitchClassSet([5, 6, 9])
    assert pcset.transpose(5) == pitchtools.NumberedChromaticPitchClassSet([6, 7, 10])
    assert pcset.transpose(6) == pitchtools.NumberedChromaticPitchClassSet([7, 8, 11])
    assert pcset.transpose(7) == pitchtools.NumberedChromaticPitchClassSet([8, 9, 0])
    assert pcset.transpose(8) == pitchtools.NumberedChromaticPitchClassSet([9, 10, 1])
    assert pcset.transpose(9) == pitchtools.NumberedChromaticPitchClassSet([10, 11, 2])
    assert pcset.transpose(10) == pitchtools.NumberedChromaticPitchClassSet([11, 0, 3])
    assert pcset.transpose(11) == pitchtools.NumberedChromaticPitchClassSet([0, 1, 4])
