from abjad import *


def test_pitchtools_all_are_named_pitch_tokens_01( ):

   assert pitchtools.all_are_named_pitch_tokens(
      [('c', 4), ('d', 4), pitchtools.NamedPitch('e', 4)])
   assert pitchtools.all_are_named_pitch_tokens([0, 2, 4])
   assert not pitchtools.all_are_named_pitch_tokens(['foo', 'bar'])
