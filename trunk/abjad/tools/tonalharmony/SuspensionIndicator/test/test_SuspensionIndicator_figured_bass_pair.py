from abjad import *


def test_SuspensionIndicator_figured_bass_pair_01( ):

   #assert tonalharmony.SuspensionIndicator(9, 8).figured_bass_pair == (9, 8)
   assert tonalharmony.SuspensionIndicator(7, 6).figured_bass_pair == (7, 6)
   assert tonalharmony.SuspensionIndicator(4, 3).figured_bass_pair == (4, 3)
   assert tonalharmony.SuspensionIndicator(2, 1).figured_bass_pair == (2, 1)
