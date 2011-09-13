from abjad import *


def test_NamedDiatonicPitchClass___init___01():
    '''Init named diatonic pitch-class with diatonic pitch-class name.
    '''

    named_diatonic_pitch_class = pitchtools.NamedDiatonicPitchClass('c')
    assert isinstance(named_diatonic_pitch_class, pitchtools.NamedDiatonicPitchClass)


def test_NamedDiatonicPitchClass___init___02():
    '''Init named diatonic pitch-class with diatonic pitch-class number.
    '''

    named_diatonic_pitch_class = pitchtools.NamedDiatonicPitchClass(0)
    assert isinstance(named_diatonic_pitch_class, pitchtools.NamedDiatonicPitchClass)


def test_NamedDiatonicPitchClass___init___03():
    '''Init named diatonic pitch-class with named diatonic pitch-class.
    '''

    named_diatonic_pitch_class_1 = pitchtools.NamedDiatonicPitchClass(0)
    named_diatonic_pitch_class_2 = pitchtools.NamedDiatonicPitchClass(named_diatonic_pitch_class_1)
    assert isinstance(named_diatonic_pitch_class_1, pitchtools.NamedDiatonicPitchClass)
    assert isinstance(named_diatonic_pitch_class_2, pitchtools.NamedDiatonicPitchClass)
