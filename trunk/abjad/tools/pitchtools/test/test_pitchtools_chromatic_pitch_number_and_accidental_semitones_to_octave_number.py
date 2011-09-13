from abjad import *


def test_pitchtools_chromatic_pitch_number_and_accidental_semitones_to_octave_number_01():

    assert pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, 0) == 5
    assert pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, -1) == 5
    assert pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, -2) == 5
    assert pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, 1) == 4
    assert pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, 2) == 4
