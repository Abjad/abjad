from abjad import *


def test_pitchtools_is_pitch_token_collection_01( ):

   assert pitchtools.is_pitch_token_collection(
      [('c', 4), ('d', 4), NamedPitch('e', 4)])
   assert pitchtools.is_pitch_token_collection([0, 2, 4])
   assert not pitchtools.is_pitch_token_collection(['foo', 'bar'])
