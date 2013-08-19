# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet_transpose_01():

    pcset = pitchtools.NumberedPitchClassSet([1, 2, 5])
    assert pcset.transpose(0) == pitchtools.NumberedPitchClassSet([1, 2, 5])
    assert pcset.transpose(1) == pitchtools.NumberedPitchClassSet([2, 3, 6])
    assert pcset.transpose(2) == pitchtools.NumberedPitchClassSet([3, 4, 7])
    assert pcset.transpose(3) == pitchtools.NumberedPitchClassSet([4, 5, 8])
    assert pcset.transpose(4) == pitchtools.NumberedPitchClassSet([5, 6, 9])
    assert pcset.transpose(5) == pitchtools.NumberedPitchClassSet([6, 7, 10])
    assert pcset.transpose(6) == pitchtools.NumberedPitchClassSet([7, 8, 11])
    assert pcset.transpose(7) == pitchtools.NumberedPitchClassSet([8, 9, 0])
    assert pcset.transpose(8) == pitchtools.NumberedPitchClassSet([9, 10, 1])
    assert pcset.transpose(9) == pitchtools.NumberedPitchClassSet([10, 11, 2])
    assert pcset.transpose(10) == pitchtools.NumberedPitchClassSet([11, 0, 3])
    assert pcset.transpose(11) == pitchtools.NumberedPitchClassSet([0, 1, 4])
