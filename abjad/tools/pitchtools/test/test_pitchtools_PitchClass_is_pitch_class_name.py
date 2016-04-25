# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClass_is_pitch_class_name_01():

    assert pitchtools.PitchClass.is_pitch_class_name('c')
    assert pitchtools.PitchClass.is_pitch_class_name('cs')
    assert pitchtools.PitchClass.is_pitch_class_name('css')
    assert pitchtools.PitchClass.is_pitch_class_name('cqs')
    assert pitchtools.PitchClass.is_pitch_class_name('ctqs')
    assert pitchtools.PitchClass.is_pitch_class_name('cf')
    assert pitchtools.PitchClass.is_pitch_class_name('cff')
    assert pitchtools.PitchClass.is_pitch_class_name('cqf')
    assert pitchtools.PitchClass.is_pitch_class_name('ctqf')


def test_pitchtools_PitchClass_is_pitch_class_name_02():

    assert not pitchtools.PitchClass.is_pitch_class_name('c,')
    assert not pitchtools.PitchClass.is_pitch_class_name("c'")
    assert not pitchtools.PitchClass.is_pitch_class_name(8)
