# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClass_is_diatonic_pitch_class_number_01():

    assert pitchtools.PitchClass.is_diatonic_pitch_class_number(0)
    assert pitchtools.PitchClass.is_diatonic_pitch_class_number(1)
    assert pitchtools.PitchClass.is_diatonic_pitch_class_number(2)
    assert pitchtools.PitchClass.is_diatonic_pitch_class_number(3)
    assert pitchtools.PitchClass.is_diatonic_pitch_class_number(4)
    assert pitchtools.PitchClass.is_diatonic_pitch_class_number(5)
    assert pitchtools.PitchClass.is_diatonic_pitch_class_number(6)


def test_pitchtools_PitchClass_is_diatonic_pitch_class_number_02():

    assert not pitchtools.PitchClass.is_diatonic_pitch_class_number(-1)
    assert not pitchtools.PitchClass.is_diatonic_pitch_class_number(7)
    assert not pitchtools.PitchClass.is_diatonic_pitch_class_number('foo')
