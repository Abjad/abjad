# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_name_to_diatonic_pitch_class_number_01():

    assert pitchtools.pitch_name_to_diatonic_pitch_class_number("cf''") == 0
    assert pitchtools.pitch_name_to_diatonic_pitch_class_number("c''") == 0
    assert pitchtools.pitch_name_to_diatonic_pitch_class_number("cs''") == 0
    assert pitchtools.pitch_name_to_diatonic_pitch_class_number("bf''") == 6
    assert pitchtools.pitch_name_to_diatonic_pitch_class_number("b''") == 6
    assert pitchtools.pitch_name_to_diatonic_pitch_class_number("bs''") == 6
