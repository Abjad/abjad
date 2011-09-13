from abjad import *


def test_NumberedChromaticPitchClass_apply_accidental_01():

    pc = pitchtools.NumberedChromaticPitchClass(11)

    assert pc.apply_accidental('sharp') == pitchtools.NumberedChromaticPitchClass(0)
    assert pc.apply_accidental('flat') == pitchtools.NumberedChromaticPitchClass(10)
    assert pc.apply_accidental('double sharp') == pitchtools.NumberedChromaticPitchClass(1)
    assert pc.apply_accidental('double flat') == pitchtools.NumberedChromaticPitchClass(9)
    assert pc.apply_accidental('quarter sharp') == pitchtools.NumberedChromaticPitchClass(11.5)
    assert pc.apply_accidental('quarter flat') == pitchtools.NumberedChromaticPitchClass(10.5)
