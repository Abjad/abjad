from abjad import *


def test_NumberedChromaticPitchClassSegment_invert_01():

    pcseg = pitchtools.NumberedChromaticPitchClassSegment([0, 6, 10, 4, 9, 2])

    assert pcseg.invert() == pitchtools.NumberedChromaticPitchClassSegment([0, 6, 2, 8, 3, 10])
