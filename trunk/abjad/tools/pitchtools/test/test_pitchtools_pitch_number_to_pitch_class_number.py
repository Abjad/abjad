# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_number_to_pitch_class_number_01():

    assert pitchtools.pitch_number_to_pitch_class_number(11) == 11
    assert pitchtools.pitch_number_to_pitch_class_number(12) == 0
    assert pitchtools.pitch_number_to_pitch_class_number(13) == 1
    assert pitchtools.pitch_number_to_pitch_class_number(23) == 11
    assert pitchtools.pitch_number_to_pitch_class_number(24) == 0
    assert pitchtools.pitch_number_to_pitch_class_number(25) == 1
