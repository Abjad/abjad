from abjad import *


def test_pitchtools_pitch_string_to_pitches_01( ):

   pitches = pitchtools.pitch_string_to_pitches("c, c c' c''")

   assert pitches == [
      Pitch('c', 2), Pitch('c', 3), Pitch('c', 4), Pitch('c', 5)]
