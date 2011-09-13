from abjad import *
import py.test


def test_NamedDiatonicPitchClass___cmp___01():
    '''Compare equal named diatonic pitch-classes.
    '''

    named_diatonic_pitch_class_1 = pitchtools.NamedDiatonicPitchClass('c')
    named_diatonic_pitch_class_2 = pitchtools.NamedDiatonicPitchClass('c')

    assert      named_diatonic_pitch_class_1 == named_diatonic_pitch_class_2
    assert not named_diatonic_pitch_class_1 != named_diatonic_pitch_class_2

    comparison_string = 'named_diatonic_pitch_class_1 <  named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 <= named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >  named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >= named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_NamedDiatonicPitchClass___cmp___02():
    '''Compare named diatonic pitch-class to equivalent diatonic pitch-class name.
    '''

    named_diatonic_pitch_class_1 = pitchtools.NamedDiatonicPitchClass('c')
    diatonic_pitch_class_name = 'c'

    assert      named_diatonic_pitch_class_1 == diatonic_pitch_class_name
    assert not named_diatonic_pitch_class_1 != diatonic_pitch_class_name

    comparison_string = 'named_diatonic_pitch_class_1 <  diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 <= diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >  diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >= diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_NamedDiatonicPitchClass___cmp___03():
    '''Compare unequal named diatonic pitch-classes.
    '''

    named_diatonic_pitch_class_1 = pitchtools.NamedDiatonicPitchClass('c')
    named_diatonic_pitch_class_2 = pitchtools.NamedDiatonicPitchClass('d')

    assert not named_diatonic_pitch_class_1 == named_diatonic_pitch_class_2
    assert      named_diatonic_pitch_class_1 != named_diatonic_pitch_class_2

    comparison_string = 'named_diatonic_pitch_class_1 <  named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 <= named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >  named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >= named_diatonic_pitch_class_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_NamedDiatonicPitchClass___cmp___04():
    '''Compare named diatonic pitch-class to unequal diatonic pitch-class name.
    '''

    named_diatonic_pitch_class_1 = pitchtools.NamedDiatonicPitchClass('c')
    diatonic_pitch_class_name = 'd'

    assert not named_diatonic_pitch_class_1 == diatonic_pitch_class_name
    assert      named_diatonic_pitch_class_1 != diatonic_pitch_class_name

    comparison_string = 'named_diatonic_pitch_class_1 <  diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 <= diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >  diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'named_diatonic_pitch_class_1 >= diatonic_pitch_class_name'
    assert py.test.raises(NotImplementedError, comparison_string)
