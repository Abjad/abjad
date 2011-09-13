from abjad import *


def test_pitchtools_octave_tick_string_to_octave_number_01():

    assert pitchtools.octave_tick_string_to_octave_number('') == 3
    assert pitchtools.octave_tick_string_to_octave_number(',') == 2
    assert pitchtools.octave_tick_string_to_octave_number(',,') == 1
    assert pitchtools.octave_tick_string_to_octave_number(',,,') == 0
    assert pitchtools.octave_tick_string_to_octave_number("'") == 4
    assert pitchtools.octave_tick_string_to_octave_number("''") == 5
    assert pitchtools.octave_tick_string_to_octave_number("'''") == 6
