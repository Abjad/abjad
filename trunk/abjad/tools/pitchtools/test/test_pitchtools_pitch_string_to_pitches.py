from abjad import *


def test_pitchtools_pitch_string_to_pitches_01( ):

   pitches = pitchtools.pitch_string_to_pitches("c, c c' c''")

   assert pitches == [
      NamedPitch('c', 2), NamedPitch('c', 3), NamedPitch('c', 4), NamedPitch('c', 5)]
