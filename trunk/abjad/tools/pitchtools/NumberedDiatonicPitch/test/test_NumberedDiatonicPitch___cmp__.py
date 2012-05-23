from abjad import *


def test_NumberedDiatonicPitch___cmp___01():
    '''Compare equal numbered diatonic pitches.
    '''

    numbered_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
    numbered_diatonic_pitch_2 = pitchtools.NumberedDiatonicPitch(7)

    assert      numbered_diatonic_pitch_1 == numbered_diatonic_pitch_2
    assert not numbered_diatonic_pitch_1 != numbered_diatonic_pitch_2
    assert not numbered_diatonic_pitch_1 <  numbered_diatonic_pitch_2
    assert      numbered_diatonic_pitch_1 <= numbered_diatonic_pitch_2
    assert not numbered_diatonic_pitch_1 >  numbered_diatonic_pitch_2
    assert      numbered_diatonic_pitch_1 >= numbered_diatonic_pitch_2


def test_NumberedDiatonicPitch___cmp___02():
    '''Compare numbered diatonic pitch to equivalent diatonic pitch number.
    '''

    numbered_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
    diatonic_pitch_number = 7

    assert      numbered_diatonic_pitch_1 == diatonic_pitch_number
    assert not numbered_diatonic_pitch_1 != diatonic_pitch_number
    assert not numbered_diatonic_pitch_1 <  diatonic_pitch_number
    assert      numbered_diatonic_pitch_1 <= diatonic_pitch_number
    assert not numbered_diatonic_pitch_1 >  diatonic_pitch_number
    assert      numbered_diatonic_pitch_1 >= diatonic_pitch_number


def test_NumberedDiatonicPitch___cmp___03():
    '''Compare unequal numbered diatonic pitches.
    '''

    numbered_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
    numbered_diatonic_pitch_2 = pitchtools.NumberedDiatonicPitch(8)

    assert not numbered_diatonic_pitch_1 == numbered_diatonic_pitch_2
    assert      numbered_diatonic_pitch_1 != numbered_diatonic_pitch_2
    assert      numbered_diatonic_pitch_1 <  numbered_diatonic_pitch_2
    assert      numbered_diatonic_pitch_1 <= numbered_diatonic_pitch_2
    assert not numbered_diatonic_pitch_1 >  numbered_diatonic_pitch_2
    assert not numbered_diatonic_pitch_1 >= numbered_diatonic_pitch_2


def test_NumberedDiatonicPitch___cmp___04():
    '''Compare numbered diatonic pitches to inequivalent diatonic pitch number.
    '''

    numbered_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
    diatonic_pitch_number = 8

    assert not numbered_diatonic_pitch_1 == diatonic_pitch_number
    assert      numbered_diatonic_pitch_1 != diatonic_pitch_number
    assert      numbered_diatonic_pitch_1 <  diatonic_pitch_number
    assert      numbered_diatonic_pitch_1 <= diatonic_pitch_number
    assert not numbered_diatonic_pitch_1 >  diatonic_pitch_number
    assert not numbered_diatonic_pitch_1 >= diatonic_pitch_number
