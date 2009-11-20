from abjad import *


def test_pitchtools_is_pair_01( ):

   assert pitchtools.is_pair(('c', 4))
   assert pitchtools.is_pair(('cs', 4))
   assert not pitchtools.is_pair('cs4')
