from abjad import *


def test_is_pitch_token_01( ):

   assert pitchtools.is_pitch_token(('cs', 4))
   assert pitchtools.is_pitch_token(Pitch('cs', 4))
   assert pitchtools.is_pitch_token(1)
   assert pitchtools.is_pitch_token(1.0)


def test_is_pitch_token_02( ):

   assert not pitchtools.is_pitch_token('foo')
