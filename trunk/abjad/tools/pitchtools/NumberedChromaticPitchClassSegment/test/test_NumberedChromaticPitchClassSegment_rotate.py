from abjad import *


def test_NumberedChromaticPitchClassSegment_rotate_01():

    pcseg = pitchtools.NumberedChromaticPitchClassSegment([0, 6, 10, 4, 9, 2])
    PCSeg = pitchtools.NumberedChromaticPitchClassSegment

    assert pcseg.rotate(0) == PCSeg([0, 6, 10, 4, 9, 2])


def test_NumberedChromaticPitchClassSegment_rotate_02():
    '''Rotate right.'''

    pcseg = pitchtools.NumberedChromaticPitchClassSegment([0, 6, 10, 4, 9, 2])
    PCSeg = pitchtools.NumberedChromaticPitchClassSegment

    assert pcseg.rotate(1) == PCSeg([2, 0, 6, 10, 4, 9])
    assert pcseg.rotate(2) == PCSeg([9, 2, 0, 6, 10, 4])
    assert pcseg.rotate(3) == PCSeg([4, 9, 2, 0, 6, 10])
    assert pcseg.rotate(4) == PCSeg([10, 4, 9, 2, 0, 6])
    assert pcseg.rotate(5) == PCSeg([6, 10, 4, 9, 2, 0])
    assert pcseg.rotate(6) == PCSeg([0, 6, 10, 4, 9, 2])


def test_NumberedChromaticPitchClassSegment_rotate_03():
    '''Rotate left.'''

    pcseg = pitchtools.NumberedChromaticPitchClassSegment([0, 6, 10, 4, 9, 2])
    PCSeg = pitchtools.NumberedChromaticPitchClassSegment

    assert pcseg.rotate(-1) == PCSeg([6, 10, 4, 9, 2, 0])
    assert pcseg.rotate(-2) == PCSeg([10, 4, 9, 2, 0, 6])
    assert pcseg.rotate(-3) == PCSeg([4, 9, 2, 0, 6, 10])
    assert pcseg.rotate(-4) == PCSeg([9, 2, 0, 6, 10, 4])
    assert pcseg.rotate(-5) == PCSeg([2, 0, 6, 10, 4, 9])
    assert pcseg.rotate(-6) == PCSeg([0, 6, 10, 4, 9, 2])
