# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_name_to_diatonic_pitch_name_01():

    assert pitchtools.pitch_name_to_diatonic_pitch_name("c''") == "c''"
    assert pitchtools.pitch_name_to_diatonic_pitch_name("cs''") == "c''"
    assert pitchtools.pitch_name_to_diatonic_pitch_name("d''") == "d''"
    assert pitchtools.pitch_name_to_diatonic_pitch_name("ef''") == "e''"
    assert pitchtools.pitch_name_to_diatonic_pitch_name("e''") == "e''"
    assert pitchtools.pitch_name_to_diatonic_pitch_name("f''") == "f''"
