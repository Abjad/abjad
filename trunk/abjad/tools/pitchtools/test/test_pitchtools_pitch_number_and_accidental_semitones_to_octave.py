from abjad import *


def test_pitchtools_pitch_number_and_accidental_semitones_to_octave_01( ):

   assert pitchtools.pitch_number_and_accidental_semitones_to_octave(12, 0) == 5
   assert pitchtools.pitch_number_and_accidental_semitones_to_octave(12, -1) == 5
   assert pitchtools.pitch_number_and_accidental_semitones_to_octave(12, -2) == 5
   assert pitchtools.pitch_number_and_accidental_semitones_to_octave(12, 1) == 4
   assert pitchtools.pitch_number_and_accidental_semitones_to_octave(12, 2) == 4

