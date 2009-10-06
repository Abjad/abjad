from abjad import *


def test_pctheory_PCSet___init__01( ):
   '''Works with numbers.'''

   assert len(pctheory.PCSet([0, 2, 6, 7])) == 4


def test_pctheory_PCSet___init__02( ):
   '''Works with PCs.'''

   assert len(pctheory.PCSet([pctheory.PC(x) for x in [0, 2, 6, 7]])) == 4
