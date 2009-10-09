from abjad import *


def test_pctheory_PCSet___eq___01( ):
   '''PCset equality works as expected.'''

   pcset1 = pctheory.PCSet([0, 2, 6, 7])
   pcset2 = pctheory.PCSet([0, 2, 6, 7])
   pcset3 = pctheory.PCSet([0, 2, 6, 8])

   assert pcset1 == pcset2
   assert pcset1 != pcset3
   assert pcset2 != pcset3 
   assert not pcset1 != pcset2
