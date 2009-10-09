from abjad import *


def test_pctheory_PCSet___contains___01( ):
   '''PCSet containment works as expected.'''

   pcset = pctheory.PCSet([0, 2, 6, 7])
   pc1 = pctheory.PC(2)
   pc2 = pctheory.PC(3)
   
   assert pc1 in pcset
   assert pc2 not in pcset
