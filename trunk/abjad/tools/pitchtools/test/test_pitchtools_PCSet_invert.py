from abjad import *


def test_pitchtools_PCSet_invert_01( ):

   assert pitchtools.PCSet([0, 1, 5]).invert( ) == pitchtools.PCSet([0, 7, 11])
   assert pitchtools.PCSet([1, 2, 6]).invert( ) == pitchtools.PCSet([6, 10, 11])
