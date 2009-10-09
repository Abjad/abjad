from abjad import *


def test_pitchtools_PCSet_invert_01( ):

   assert pitchtools.PCSet([0, 1, 5]).multiply(5) == \
      pitchtools.PCSet([0, 1, 5])
   assert pitchtools.PCSet([1, 2, 6]).multiply(5) == \
      pitchtools.PCSet([5, 6, 10])
   assert pitchtools.PCSet([2, 3, 7]).multiply(5) == \
      pitchtools.PCSet([3, 10, 11])
