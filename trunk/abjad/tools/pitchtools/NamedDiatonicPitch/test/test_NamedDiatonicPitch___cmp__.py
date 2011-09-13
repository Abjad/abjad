from abjad import *


def test_NamedDiatonicPitch___cmp___01():
    '''Compare equal named diatonic pitches.
    '''

    named_diatonic_pitch_1 = pitchtools.NamedDiatonicPitch("c''")
    named_diatonic_pitch_2 = pitchtools.NamedDiatonicPitch("c''")

    assert      named_diatonic_pitch_1 == named_diatonic_pitch_2
    assert not named_diatonic_pitch_1 != named_diatonic_pitch_2
    assert not named_diatonic_pitch_1 <  named_diatonic_pitch_2
    assert      named_diatonic_pitch_1 <= named_diatonic_pitch_2
    assert not named_diatonic_pitch_1 >  named_diatonic_pitch_2
    assert      named_diatonic_pitch_1 >= named_diatonic_pitch_2


def test_NamedDiatonicPitch___cmp___02():
    '''Compare named diatonic pitch to equivalent diatonic pitch name.
    '''

    named_diatonic_pitch_1 = pitchtools.NamedDiatonicPitch("c''")
    diatonic_pitch_name = "c''"

    assert      named_diatonic_pitch_1 == diatonic_pitch_name
    assert not named_diatonic_pitch_1 != diatonic_pitch_name
    assert not named_diatonic_pitch_1 <  diatonic_pitch_name
    assert      named_diatonic_pitch_1 <= diatonic_pitch_name
    assert not named_diatonic_pitch_1 >  diatonic_pitch_name
    assert      named_diatonic_pitch_1 >= diatonic_pitch_name


def test_NamedDiatonicPitch___cmp___03():
    '''Compare unequal numbered diatonic pitches.
    '''

    named_diatonic_pitch_1 = pitchtools.NamedDiatonicPitch("c''")
    named_diatonic_pitch_2 = pitchtools.NamedDiatonicPitch("d''")

    assert not named_diatonic_pitch_1 == named_diatonic_pitch_2
    assert      named_diatonic_pitch_1 != named_diatonic_pitch_2
    assert      named_diatonic_pitch_1 <  named_diatonic_pitch_2
    assert      named_diatonic_pitch_1 <= named_diatonic_pitch_2
    assert not named_diatonic_pitch_1 >  named_diatonic_pitch_2
    assert not named_diatonic_pitch_1 >= named_diatonic_pitch_2


def test_NamedDiatonicPitch___cmp___04():
    '''Compare numbered diatonic pitches to inequivalent diatonic pitch name.
    '''

    named_diatonic_pitch_1 = pitchtools.NamedDiatonicPitch("c''")
    diatonic_pitch_name = 8

    assert not named_diatonic_pitch_1 == diatonic_pitch_name
    assert      named_diatonic_pitch_1 != diatonic_pitch_name
    assert      named_diatonic_pitch_1 <  diatonic_pitch_name
    assert      named_diatonic_pitch_1 <= diatonic_pitch_name
    assert not named_diatonic_pitch_1 >  diatonic_pitch_name
    assert not named_diatonic_pitch_1 >= diatonic_pitch_name
