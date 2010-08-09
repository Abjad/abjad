from abjad import *


def test_pitchtools_pitch_name_input_string_to_named_pitch_list_01( ):

   pitches = pitchtools.pitch_name_input_string_to_named_pitch_list("c, c c' c''")

   assert pitches == [pitchtools.NamedPitch('c', 2), pitchtools.NamedPitch('c', 3), 
      pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('c', 5)]
