from abjad import *


def test_pitchtools_is_pitch_pair_01( ):

   assert pitchtools.is_pitch_pair(('c', 4))
   assert pitchtools.is_pitch_pair(('cs', 4))
   assert not pitchtools.is_pitch_pair('cs4')
