from abjad import *


def test_pitchtools_pitch_string_to_octave_number_01( ):

   assert pitchtools.pitch_string_to_octave_number("cs'") == 4
   assert pitchtools.pitch_string_to_octave_number('cs') == 3
   assert pitchtools.pitch_string_to_octave_number('cs,') == 2
