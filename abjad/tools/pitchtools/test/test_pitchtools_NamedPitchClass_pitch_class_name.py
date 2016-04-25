# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass_pitch_class_name_01():

    assert pitchtools.NamedPitchClass("c''").pitch_class_name == 'c'
    assert pitchtools.NamedPitchClass("d''").pitch_class_name == 'd'
    assert pitchtools.NamedPitchClass("e''").pitch_class_name == 'e'
    assert pitchtools.NamedPitchClass("f''").pitch_class_name == 'f'
