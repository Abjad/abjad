from abjad import *


def test_NumberedChromaticPitchClassSegment___rmul___01():

    ncpcs1 = pitchtools.NumberedChromaticPitchClassSegment([0, 1, 11, 9])
    ncpsc2 = 2 * ncpcs1

    assert ncpsc2 == pitchtools.NumberedChromaticPitchClassSegment([0, 1, 11, 9, 0, 1, 11, 9])
