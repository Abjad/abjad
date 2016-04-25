# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass_diatonic_pitch_class_name_01():

    assert pitchtools.NamedPitchClass('c').diatonic_pitch_class_name == 'c'
    assert pitchtools.NamedPitchClass('cs').diatonic_pitch_class_name == 'c'
    assert pitchtools.NamedPitchClass('cf').diatonic_pitch_class_name == 'c'
    assert pitchtools.NamedPitchClass('cqs').diatonic_pitch_class_name == 'c'
    assert pitchtools.NamedPitchClass('cqf').diatonic_pitch_class_name == 'c'
