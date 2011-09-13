from abjad import *


def test_pitchtools_is_diatonic_pitch_class_number_01():

    assert pitchtools.is_diatonic_pitch_class_number(0)
    assert pitchtools.is_diatonic_pitch_class_number(1)
    assert pitchtools.is_diatonic_pitch_class_number(2)
    assert pitchtools.is_diatonic_pitch_class_number(3)
    assert pitchtools.is_diatonic_pitch_class_number(4)
    assert pitchtools.is_diatonic_pitch_class_number(5)
    assert pitchtools.is_diatonic_pitch_class_number(6)


def test_pitchtools_is_diatonic_pitch_class_number_02():

    assert not pitchtools.is_diatonic_pitch_class_number(-1)
    assert not pitchtools.is_diatonic_pitch_class_number(7)
    assert not pitchtools.is_diatonic_pitch_class_number('foo')
