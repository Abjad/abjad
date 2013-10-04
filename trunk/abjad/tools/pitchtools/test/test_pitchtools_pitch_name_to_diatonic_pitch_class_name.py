# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_name_to_diatonic_pitch_class_name_01():

    assert pitchtools.pitch_name_to_diatonic_pitch_class_name("c''") == 'c'
    assert pitchtools.pitch_name_to_diatonic_pitch_class_name("cs''") == 'c'
    assert pitchtools.pitch_name_to_diatonic_pitch_class_name("d''") == 'd'
    assert pitchtools.pitch_name_to_diatonic_pitch_class_name("ef''") == 'e'
    assert pitchtools.pitch_name_to_diatonic_pitch_class_name("e''") == 'e'
    assert pitchtools.pitch_name_to_diatonic_pitch_class_name("f''") == 'f'
