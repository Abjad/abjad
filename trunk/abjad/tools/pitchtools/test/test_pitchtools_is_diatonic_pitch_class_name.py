from abjad import *


def test_pitchtools_is_diatonic_pitch_class_name_01():

    assert pitchtools.is_diatonic_pitch_class_name('c')
    assert pitchtools.is_diatonic_pitch_class_name('d')
    assert pitchtools.is_diatonic_pitch_class_name('e')
    assert pitchtools.is_diatonic_pitch_class_name('f')
    assert pitchtools.is_diatonic_pitch_class_name('g')
    assert pitchtools.is_diatonic_pitch_class_name('a')
    assert pitchtools.is_diatonic_pitch_class_name('b')


def test_pitchtools_is_diatonic_pitch_class_name_02():

    assert pitchtools.is_diatonic_pitch_class_name('C')
    assert pitchtools.is_diatonic_pitch_class_name('D')
    assert pitchtools.is_diatonic_pitch_class_name('E')
    assert pitchtools.is_diatonic_pitch_class_name('F')
    assert pitchtools.is_diatonic_pitch_class_name('G')
    assert pitchtools.is_diatonic_pitch_class_name('A')
    assert pitchtools.is_diatonic_pitch_class_name('B')


def test_pitchtools_is_diatonic_pitch_class_name_03():

    assert not pitchtools.is_diatonic_pitch_class_name(8)
