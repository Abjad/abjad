# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch_pitch_class_number_01():

    assert NamedPitch('c').pitch_class_number == 0
    assert NamedPitch('d').pitch_class_number == 2
    assert NamedPitch('e').pitch_class_number == 4
    assert NamedPitch('f').pitch_class_number == 5
    assert NamedPitch('g').pitch_class_number == 7
    assert NamedPitch('a').pitch_class_number == 9
    assert NamedPitch('b').pitch_class_number == 11


def test_pitchtools_NamedPitch_pitch_class_number_02():

    assert NamedPitch('cff').pitch_class_number == 10
    assert NamedPitch('ctqf').pitch_class_number == 10.5
    assert NamedPitch('cf').pitch_class_number == 11
    assert NamedPitch('cqf').pitch_class_number == 11.5
    assert NamedPitch('c').pitch_class_number == 0
    assert NamedPitch('cqs').pitch_class_number == 0.5
    assert NamedPitch('cs').pitch_class_number == 1
    assert NamedPitch('ctqs').pitch_class_number == 1.5
    assert NamedPitch('css').pitch_class_number == 2


def test_pitchtools_NamedPitch_pitch_class_number_03():

    assert NamedPitch("cf''").pitch_class_number == 11
    assert NamedPitch("c''").pitch_class_number == 0
    assert NamedPitch("cs''").pitch_class_number == 1
    assert NamedPitch("bf''").pitch_class_number == 10
    assert NamedPitch("b''").pitch_class_number == 11
    assert NamedPitch("bs''").pitch_class_number == 0
