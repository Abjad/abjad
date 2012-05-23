from abjad import *


def test_NumberedChromaticPitchClass_multiply_01():

    assert pitchtools.NumberedChromaticPitchClass(0).multiply(5) == pitchtools.NumberedChromaticPitchClass(0)
    assert pitchtools.NumberedChromaticPitchClass(1).multiply(5) == pitchtools.NumberedChromaticPitchClass(5)
    assert pitchtools.NumberedChromaticPitchClass(2).multiply(5) == pitchtools.NumberedChromaticPitchClass(10)
    assert pitchtools.NumberedChromaticPitchClass(3).multiply(5) == pitchtools.NumberedChromaticPitchClass(3)
    assert pitchtools.NumberedChromaticPitchClass(4).multiply(5) == pitchtools.NumberedChromaticPitchClass(8)
    assert pitchtools.NumberedChromaticPitchClass(5).multiply(5) == pitchtools.NumberedChromaticPitchClass(1)
    assert pitchtools.NumberedChromaticPitchClass(6).multiply(5) == pitchtools.NumberedChromaticPitchClass(6)
    assert pitchtools.NumberedChromaticPitchClass(7).multiply(5) == pitchtools.NumberedChromaticPitchClass(11)
    assert pitchtools.NumberedChromaticPitchClass(8).multiply(5) == pitchtools.NumberedChromaticPitchClass(4)
    assert pitchtools.NumberedChromaticPitchClass(9).multiply(5) == pitchtools.NumberedChromaticPitchClass(9)
    assert pitchtools.NumberedChromaticPitchClass(10).multiply(5) == pitchtools.NumberedChromaticPitchClass(2)
    assert pitchtools.NumberedChromaticPitchClass(11).multiply(5) == pitchtools.NumberedChromaticPitchClass(7)
