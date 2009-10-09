from abjad import *


def test_pitchtools_PCSet___contains___01( ):
   '''PCSet containment works as expected.'''

   pcset = pitchtools.PCSet([0, 2, 6, 7])
   pc1 = pitchtools.PC(2)
   pc2 = pitchtools.PC(3)
   
   assert pc1 in pcset
   assert pc2 not in pcset
