# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_name_to_pitch_class_number_01():

    assert pitchtools.pitch_name_to_pitch_class_number("cf''") == 11
    assert pitchtools.pitch_name_to_pitch_class_number("c''") == 0
    assert pitchtools.pitch_name_to_pitch_class_number("cs''") == 1
    assert pitchtools.pitch_name_to_pitch_class_number("bf''") == 10
    assert pitchtools.pitch_name_to_pitch_class_number("b''") == 11
    assert pitchtools.pitch_name_to_pitch_class_number("bs''") == 0
