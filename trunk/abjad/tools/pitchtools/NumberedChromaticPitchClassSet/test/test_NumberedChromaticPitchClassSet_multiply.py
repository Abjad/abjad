from abjad import *


def test_NumberedChromaticPitchClassSet_multiply_01():

    assert pitchtools.NumberedChromaticPitchClassSet([0, 1, 5]).multiply(5) == \
        pitchtools.NumberedChromaticPitchClassSet([0, 1, 5])
    assert pitchtools.NumberedChromaticPitchClassSet([1, 2, 6]).multiply(5) == \
        pitchtools.NumberedChromaticPitchClassSet([5, 6, 10])
    assert pitchtools.NumberedChromaticPitchClassSet([2, 3, 7]).multiply(5) == \
        pitchtools.NumberedChromaticPitchClassSet([3, 10, 11])
