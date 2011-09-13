from abjad import *


def test_NumberedDiatonicPitchClass___init___01():
    '''Init numbered diatonic pitch-class from diatonic pitch-class number.
    '''

    numbered_diatonic_pitch_class = pitchtools.NumberedDiatonicPitchClass(0)
    assert isinstance(numbered_diatonic_pitch_class, pitchtools.NumberedDiatonicPitchClass)

    numbered_diatonic_pitch_class = pitchtools.NumberedDiatonicPitchClass(0.0)
    assert isinstance(numbered_diatonic_pitch_class, pitchtools.NumberedDiatonicPitchClass)

    numbered_diatonic_pitch_class = pitchtools.NumberedDiatonicPitchClass(Fraction(0))
    assert isinstance(numbered_diatonic_pitch_class, pitchtools.NumberedDiatonicPitchClass)


def test_NumberedDiatonicPitchClass___init___02():
    '''Init numbered diatonic pitch-class from diatonic pitch-class name.
    '''

    diatonic_pitch_class = pitchtools.NumberedDiatonicPitchClass('c')
    assert isinstance(diatonic_pitch_class, pitchtools.NumberedDiatonicPitchClass)


def test_NumberedDiatonicPitchClass___init___03():
    '''Init numbered diatonic pitch-class from diatonic pitch-class.
    '''

    diatonic_pitch_class_1 = pitchtools.NumberedDiatonicPitchClass(0)
    diatonic_pitch_class_2 = pitchtools.NumberedDiatonicPitchClass(diatonic_pitch_class_1)
    assert isinstance(diatonic_pitch_class_2, pitchtools.NumberedDiatonicPitchClass)
