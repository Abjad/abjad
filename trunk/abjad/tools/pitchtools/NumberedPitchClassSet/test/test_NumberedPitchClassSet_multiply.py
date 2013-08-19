# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet_multiply_01():

    assert pitchtools.NumberedPitchClassSet([0, 1, 5]).multiply(5) == \
        pitchtools.NumberedPitchClassSet([0, 1, 5])
    assert pitchtools.NumberedPitchClassSet([1, 2, 6]).multiply(5) == \
        pitchtools.NumberedPitchClassSet([5, 6, 10])
    assert pitchtools.NumberedPitchClassSet([2, 3, 7]).multiply(5) == \
        pitchtools.NumberedPitchClassSet([3, 10, 11])
