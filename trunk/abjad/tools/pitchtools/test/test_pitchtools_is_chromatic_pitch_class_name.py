from abjad import *


def test_pitchtools_is_chromatic_pitch_class_name_01():

    assert pitchtools.is_chromatic_pitch_class_name('c')
    assert pitchtools.is_chromatic_pitch_class_name('cs')
    assert pitchtools.is_chromatic_pitch_class_name('css')
    assert pitchtools.is_chromatic_pitch_class_name('cqs')
    assert pitchtools.is_chromatic_pitch_class_name('ctqs')
    assert pitchtools.is_chromatic_pitch_class_name('cf')
    assert pitchtools.is_chromatic_pitch_class_name('cff')
    assert pitchtools.is_chromatic_pitch_class_name('cqf')
    assert pitchtools.is_chromatic_pitch_class_name('ctqf')


def test_pitchtools_is_chromatic_pitch_class_name_02():

    assert not pitchtools.is_chromatic_pitch_class_name('c,')
    assert not pitchtools.is_chromatic_pitch_class_name("c'")
    assert not pitchtools.is_chromatic_pitch_class_name(8)
