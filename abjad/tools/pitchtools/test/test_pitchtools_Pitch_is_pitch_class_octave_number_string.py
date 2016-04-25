# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Pitch_is_pitch_class_octave_number_string_01():

    assert pitchtools.Pitch.is_pitch_class_octave_number_string('C#2')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('A0')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('Bb-1')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('A#10')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('D2')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('Gb4')


def test_pitchtools_Pitch_is_pitch_class_octave_number_string_02():

    assert pitchtools.Pitch.is_pitch_class_octave_number_string('C#+2')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('A~0')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('Bb~-1')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('A+10')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('Db~2')
    assert pitchtools.Pitch.is_pitch_class_octave_number_string('G+4')


def test_pitchtools_Pitch_is_pitch_class_octave_number_string_03():

    assert not pitchtools.Pitch.is_pitch_class_octave_number_string('')
    assert not pitchtools.Pitch.is_pitch_class_octave_number_string('f,,')
    assert not pitchtools.Pitch.is_pitch_class_octave_number_string("f''")
    assert not pitchtools.Pitch.is_pitch_class_octave_number_string(True)
