# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_number_to_pitch_name_01():

    assert pitchtools.pitch_number_to_pitch_name(13, 'mixed') == "cs''"
    assert pitchtools.pitch_number_to_pitch_name(14, 'mixed') == "d''"
    assert pitchtools.pitch_number_to_pitch_name(15, 'mixed') == "ef''"
    assert pitchtools.pitch_number_to_pitch_name(16, 'mixed') == "e''"
    assert pitchtools.pitch_number_to_pitch_name(17, 'mixed') == "f''"
