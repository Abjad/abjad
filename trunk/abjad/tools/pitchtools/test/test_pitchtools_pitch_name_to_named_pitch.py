from abjad import *


def test_pitchtools_pitch_name_to_named_pitch_01( ):

   pitch = pitchtools.pitch_name_to_named_pitch("css''")
   assert pitch == pitchtools.NamedPitch("css''")
