from abjad import *


def test_pitchtools_nearest_neighbor_01( ):

   assert pitchtools.nearest_neighbor(12, 0) == 12
   assert pitchtools.nearest_neighbor(12, 1) == 13
   assert pitchtools.nearest_neighbor(12, 2) == 14 
   assert pitchtools.nearest_neighbor(12, 3) == 15
   assert pitchtools.nearest_neighbor(12, 4) == 16
   assert pitchtools.nearest_neighbor(12, 5) == 17


def test_pitchtools_nearest_neighbor_02( ):

   assert pitchtools.nearest_neighbor(12, 6) == 6
   assert pitchtools.nearest_neighbor(12, 7) == 7
   assert pitchtools.nearest_neighbor(12, 8) == 8
   assert pitchtools.nearest_neighbor(12, 9) == 9
   assert pitchtools.nearest_neighbor(12, 10) == 10
   assert pitchtools.nearest_neighbor(12, 11) == 11
