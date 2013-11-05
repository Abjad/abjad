# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClass_is_pitch_class_number_01():

    assert pitchtools.PitchClass.is_pitch_class_number(0)
    assert pitchtools.PitchClass.is_pitch_class_number(0.5)
    assert pitchtools.PitchClass.is_pitch_class_number(11)
    assert pitchtools.PitchClass.is_pitch_class_number(11.5)


def test_pitchtools_PitchClass_is_pitch_class_number_02():

    assert not pitchtools.PitchClass.is_pitch_class_number(-1)
    assert not pitchtools.PitchClass.is_pitch_class_number(-0.5)
    assert not pitchtools.PitchClass.is_pitch_class_number(12)
    assert not pitchtools.PitchClass.is_pitch_class_number(99)
    assert not pitchtools.PitchClass.is_pitch_class_number('foo')
