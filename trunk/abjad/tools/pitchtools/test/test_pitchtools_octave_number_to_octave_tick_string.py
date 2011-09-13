from abjad import *


def test_pitchtools_octave_number_to_octave_tick_string_01():


    assert pitchtools.octave_number_to_octave_tick_string(-1) == ',,,,'
    assert pitchtools.octave_number_to_octave_tick_string(0) == ',,,'
    assert pitchtools.octave_number_to_octave_tick_string(1) == ',,'
    assert pitchtools.octave_number_to_octave_tick_string(2) == ','
    assert pitchtools.octave_number_to_octave_tick_string(3) == ''
    assert pitchtools.octave_number_to_octave_tick_string(4) == "'"
    assert pitchtools.octave_number_to_octave_tick_string(5) == "''"
    assert pitchtools.octave_number_to_octave_tick_string(6) == "'''"
    assert pitchtools.octave_number_to_octave_tick_string(7) == "''''"
