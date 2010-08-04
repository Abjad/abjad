from abjad import *


def test_pitchtools_pitch_string_to_pitch_01( ):

   pitch = pitchtools.pitch_string_to_pitch("css''")
   assert pitch == NamedPitch("css''")
