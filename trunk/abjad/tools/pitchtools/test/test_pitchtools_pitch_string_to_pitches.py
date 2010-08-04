from abjad import *


def test_pitchtools_pitch_string_to_pitches_01( ):

   pitches = pitchtools.pitch_string_to_pitches("c, c c' c''")

   assert pitches == [
      pitchtools.NamedPitch('c', 2), pitchtools.NamedPitch('c', 3), pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('c', 5)]
