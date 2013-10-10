# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_pitch_class_number_01():

    assert pitchtools.NamedPitch('c').pitch_class_number == 0
    assert pitchtools.NamedPitch('d').pitch_class_number == 2
    assert pitchtools.NamedPitch('e').pitch_class_number == 4
    assert pitchtools.NamedPitch('f').pitch_class_number == 5
    assert pitchtools.NamedPitch('g').pitch_class_number == 7
    assert pitchtools.NamedPitch('a').pitch_class_number == 9
    assert pitchtools.NamedPitch('b').pitch_class_number == 11


def test_NamedPitch_pitch_class_number_02():

    assert pitchtools.NamedPitch('cff').pitch_class_number == 10
    assert pitchtools.NamedPitch('ctqf').pitch_class_number == 10.5
    assert pitchtools.NamedPitch('cf').pitch_class_number == 11
    assert pitchtools.NamedPitch('cqf').pitch_class_number == 11.5
    assert pitchtools.NamedPitch('c').pitch_class_number == 0
    assert pitchtools.NamedPitch('cqs').pitch_class_number == 0.5
    assert pitchtools.NamedPitch('cs').pitch_class_number == 1
    assert pitchtools.NamedPitch('ctqs').pitch_class_number == 1.5
    assert pitchtools.NamedPitch('css').pitch_class_number == 2


def test_NamedPitch_pitch_class_number_03():

    assert pitchtools.NamedPitch("cf''").pitch_class_number == 11
    assert pitchtools.NamedPitch("c''").pitch_class_number == 0
    assert pitchtools.NamedPitch("cs''").pitch_class_number == 1
    assert pitchtools.NamedPitch("bf''").pitch_class_number == 10
    assert pitchtools.NamedPitch("b''").pitch_class_number == 11
    assert pitchtools.NamedPitch("bs''").pitch_class_number == 0
