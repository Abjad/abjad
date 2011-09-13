from abjad import *
import py.test


def test_NumberedDiatonicPitchClass___cmp___01():
    '''Compare equal numbered diatonic pitch-classes.
    '''

    numbered_diatonic_pitch_class_1 = pitchtools.NumberedDiatonicPitchClass(0)
    numbered_diatonic_pitch_class_2 = pitchtools.NumberedDiatonicPitchClass(0)

    assert      numbered_diatonic_pitch_class_1 == numbered_diatonic_pitch_class_2
    assert not numbered_diatonic_pitch_class_1 != numbered_diatonic_pitch_class_2

    comparison_string = 'numbered_diatonic_pitch_class_1 <  numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 <= numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >  numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >= numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_NumberedDiatonicPitchClass___cmp___02():
    '''Compare numbered diatonic pitch-class to equivalent diatonic pitch-class number.
    '''

    numbered_diatonic_pitch_class_1 = pitchtools.NumberedDiatonicPitchClass(0)
    diatonic_pitch_class_number = 0

    assert      numbered_diatonic_pitch_class_1 == diatonic_pitch_class_number
    assert not numbered_diatonic_pitch_class_1 != diatonic_pitch_class_number

    comparison_string = 'numbered_diatonic_pitch_class_1 <  diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 <= diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >  diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >= diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_NumberedDiatonicPitchClass___cmp___03():
    '''Compare unequal numbered diatonic pitch-classes.
    '''

    numbered_diatonic_pitch_class_1 = pitchtools.NumberedDiatonicPitchClass(0)
    numbered_diatonic_pitch_class_2 = pitchtools.NumberedDiatonicPitchClass(1)

    assert not numbered_diatonic_pitch_class_1 == numbered_diatonic_pitch_class_2
    assert      numbered_diatonic_pitch_class_1 != numbered_diatonic_pitch_class_2

    comparison_string = 'numbered_diatonic_pitch_class_1 <  numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 <= numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >  numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >= numbered_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_NumberedDiatonicPitchClass___cmp___04():
    '''Compare numbered diatonic pitch-class to unequal diatonic pitch-class number.
    '''

    numbered_diatonic_pitch_class_1 = pitchtools.NumberedDiatonicPitchClass(0)
    diatonic_pitch_class_number = 1

    assert not numbered_diatonic_pitch_class_1 == diatonic_pitch_class_number
    assert      numbered_diatonic_pitch_class_1 != diatonic_pitch_class_number

    comparison_string = 'numbered_diatonic_pitch_class_1 <  diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 <= diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >  diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'numbered_diatonic_pitch_class_1 >= diatonic_pitch_class_number'
    assert py.test.raises(NotImplementedError, comparison_string)
