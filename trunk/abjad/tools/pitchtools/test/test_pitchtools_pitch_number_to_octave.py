from abjad import *


def test_pitchtools_pitch_number_to_octave_01( ):

   assert pitchtools.pitch_number_to_octave(-12) == 3
   assert pitchtools.pitch_number_to_octave(-11) == 3
   assert pitchtools.pitch_number_to_octave(0) == 4
   assert pitchtools.pitch_number_to_octave(1) == 4
   assert pitchtools.pitch_number_to_octave(12) == 5
   assert pitchtools.pitch_number_to_octave(13) == 5
