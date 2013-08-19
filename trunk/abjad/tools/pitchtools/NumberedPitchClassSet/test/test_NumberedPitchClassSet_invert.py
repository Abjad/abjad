# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet_invert_01():

    assert pitchtools.NumberedPitchClassSet([0, 1, 5]).invert() == \
        pitchtools.NumberedPitchClassSet([0, 7, 11])
    assert pitchtools.NumberedPitchClassSet([1, 2, 6]).invert() == \
        pitchtools.NumberedPitchClassSet([6, 10, 11])
