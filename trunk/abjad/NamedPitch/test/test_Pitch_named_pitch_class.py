from abjad import *


def test_Pitch_named_pitch_class_01( ):

   pitch = NamedPitch('cs', 4)
   assert pitch.named_pitch_class == pitchtools.NamedPitchClass('cs')
