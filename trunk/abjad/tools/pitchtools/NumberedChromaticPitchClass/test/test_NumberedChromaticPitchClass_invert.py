from abjad import *


def test_NumberedChromaticPitchClass_invert_01():

    assert pitchtools.NumberedChromaticPitchClass(0).invert() == pitchtools.NumberedChromaticPitchClass(0)
    assert pitchtools.NumberedChromaticPitchClass(1).invert() == pitchtools.NumberedChromaticPitchClass(11)
    assert pitchtools.NumberedChromaticPitchClass(2).invert() == pitchtools.NumberedChromaticPitchClass(10)
    assert pitchtools.NumberedChromaticPitchClass(3).invert() == pitchtools.NumberedChromaticPitchClass(9)
    assert pitchtools.NumberedChromaticPitchClass(4).invert() == pitchtools.NumberedChromaticPitchClass(8)
    assert pitchtools.NumberedChromaticPitchClass(5).invert() == pitchtools.NumberedChromaticPitchClass(7)
    assert pitchtools.NumberedChromaticPitchClass(6).invert() == pitchtools.NumberedChromaticPitchClass(6)
    assert pitchtools.NumberedChromaticPitchClass(7).invert() == pitchtools.NumberedChromaticPitchClass(5)
    assert pitchtools.NumberedChromaticPitchClass(8).invert() == pitchtools.NumberedChromaticPitchClass(4)
    assert pitchtools.NumberedChromaticPitchClass(9).invert() == pitchtools.NumberedChromaticPitchClass(3)
    assert pitchtools.NumberedChromaticPitchClass(10).invert() == pitchtools.NumberedChromaticPitchClass(2)
    assert pitchtools.NumberedChromaticPitchClass(11).invert() == pitchtools.NumberedChromaticPitchClass(1)
