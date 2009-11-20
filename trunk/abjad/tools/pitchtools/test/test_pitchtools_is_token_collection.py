from abjad import *


def test_pitchtools_is_token_collection_01( ):

   assert pitchtools.is_token_collection([('c', 4), ('d', 4), Pitch('e', 4)])
   assert pitchtools.is_token_collection([0, 2, 4])
   assert not pitchtools.is_token_collection(['foo', 'bar'])
