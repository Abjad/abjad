# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_name_to_pitch_number_01():

    assert pitchtools.pitch_name_to_pitch_number("cff''") == 10
    assert pitchtools.pitch_name_to_pitch_number("ctqf''") == 10.5
    assert pitchtools.pitch_name_to_pitch_number("cf''") == 11
    assert pitchtools.pitch_name_to_pitch_number("cqf''") == 11.5
    assert pitchtools.pitch_name_to_pitch_number("c''") == 12
    assert pitchtools.pitch_name_to_pitch_number("cqs''") == 12.5
    assert pitchtools.pitch_name_to_pitch_number("cs''") == 13
    assert pitchtools.pitch_name_to_pitch_number("ctqs''") == 13.5
    assert pitchtools.pitch_name_to_pitch_number("css''") == 14

    assert pitchtools.pitch_name_to_pitch_number("d''") == 14
