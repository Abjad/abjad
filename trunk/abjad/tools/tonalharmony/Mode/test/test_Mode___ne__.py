from abjad import *


def test_Mode___ne___01( ):

   mode_1 = tonalharmony.Mode('dorian')
   mode_2 = tonalharmony.Mode('dorian')
   mode_3 = tonalharmony.Mode('phrygian')

   assert not mode_1 != mode_1
   assert not mode_1 != mode_2
   assert     mode_1 != mode_3
   assert not mode_2 != mode_1
   assert not mode_2 != mode_2
   assert     mode_2 != mode_3
   assert     mode_3 != mode_1
   assert     mode_3 != mode_2
   assert not mode_3 != mode_3
