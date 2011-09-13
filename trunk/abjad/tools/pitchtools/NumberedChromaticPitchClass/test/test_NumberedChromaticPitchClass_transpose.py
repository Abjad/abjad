from abjad import *


def test_NumberedChromaticPitchClass_transpose_01():

    pc = pitchtools.NumberedChromaticPitchClass(1)
    assert pc.transpose(0) == pitchtools.NumberedChromaticPitchClass(1)
    assert pc.transpose(1) == pitchtools.NumberedChromaticPitchClass(2)
    assert pc.transpose(-1) == pitchtools.NumberedChromaticPitchClass(0)
    assert pc.transpose(99) == pitchtools.NumberedChromaticPitchClass(4)
    assert pc.transpose(-99) == pitchtools.NumberedChromaticPitchClass(10)
