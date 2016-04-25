# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClass_is_diatonic_pitch_class_name_01():

    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('c')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('d')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('e')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('f')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('g')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('a')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('b')


def test_pitchtools_PitchClass_is_diatonic_pitch_class_name_02():

    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('C')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('D')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('E')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('F')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('G')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('A')
    assert pitchtools.PitchClass.is_diatonic_pitch_class_name('B')


def test_pitchtools_PitchClass_is_diatonic_pitch_class_name_03():

    assert not pitchtools.PitchClass.is_diatonic_pitch_class_name(8)
