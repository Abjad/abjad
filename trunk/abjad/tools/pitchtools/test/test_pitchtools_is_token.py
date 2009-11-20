from abjad import *


def test_pitchtools_is_token_01( ):

   assert pitchtools.is_token(('c', 4))
   assert pitchtools.is_token(Pitch('c', 4))
   assert not pitchtools.is_token('foo')
