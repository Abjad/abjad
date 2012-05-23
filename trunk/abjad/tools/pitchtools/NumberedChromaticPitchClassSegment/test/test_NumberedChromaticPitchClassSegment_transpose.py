from abjad import *


def test_NumberedChromaticPitchClassSegment_transpose_01():

    pcseg = pitchtools.NumberedChromaticPitchClassSegment([0, 6, 10, 4, 9, 2])
    PCSeg = pitchtools.NumberedChromaticPitchClassSegment

    assert pcseg.transpose(0) == PCSeg([0, 6, 10, 4, 9, 2])
    assert pcseg.transpose(1) == PCSeg([1, 7, 11, 5, 10, 3])
    assert pcseg.transpose(2) == PCSeg([2, 8, 0, 6, 11, 4])
    assert pcseg.transpose(3) == PCSeg([3, 9, 1, 7, 0, 5])
    assert pcseg.transpose(4) == PCSeg([4, 10, 2, 8, 1, 6])
    assert pcseg.transpose(5) == PCSeg([5, 11, 3, 9, 2, 7])
