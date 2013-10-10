# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass_pitch_class_number_01():

    assert pitchtools.NamedPitchClass('c').pitch_class_number == 0
    assert pitchtools.NamedPitchClass('d').pitch_class_number == 2
    assert pitchtools.NamedPitchClass('e').pitch_class_number == 4
    assert pitchtools.NamedPitchClass('f').pitch_class_number == 5
    assert pitchtools.NamedPitchClass('g').pitch_class_number == 7
    assert pitchtools.NamedPitchClass('a').pitch_class_number == 9
    assert pitchtools.NamedPitchClass('b').pitch_class_number == 11


def test_pitchtools_NamedPitchClass_pitch_class_number_01():

    assert pitchtools.NamedPitchClass('cff').pitch_class_number == 10
    assert pitchtools.NamedPitchClass('ctqf').pitch_class_number == 10.5
    assert pitchtools.NamedPitchClass('cf').pitch_class_number == 11
    assert pitchtools.NamedPitchClass('cqf').pitch_class_number == 11.5
    assert pitchtools.NamedPitchClass('c').pitch_class_number == 0
    assert pitchtools.NamedPitchClass('cqs').pitch_class_number == 0.5
    assert pitchtools.NamedPitchClass('cs').pitch_class_number == 1
    assert pitchtools.NamedPitchClass('ctqs').pitch_class_number == 1.5
    assert pitchtools.NamedPitchClass('css').pitch_class_number == 2
