from abjad import *


def test_pitchtools_pitch_class_octave_number_string_to_chromatic_pitch_name_01():

    assert pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name('C#+2') == 'ctqs,'
    assert pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name('A4') == "a'"
    assert pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name('Dbb6') == "dff'''"
    assert pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name('C-1') == 'c,,,,'
