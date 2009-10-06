from abjad import *


def test_pctheory_PC___cmp__01( ):
   '''All six comparison operators work as expected
   on different-valued PCs.'''

   pc1 = pctheory.PC(6)
   pc2 = pctheory.PC(7)

   assert not pc1 == pc2
   assert     pc1 != pc2
   assert     pc1 <  pc2
   assert     pc1 <= pc2
   assert not pc1 >  pc2
   assert not pc1 >= pc2


def test_pctheory_PC___cmp__02( ):
   '''All six comparison operators work as expected
   on same-valued PCs.'''

   pc1 = pctheory.PC(6)
   pc2 = pctheory.PC(6)

   assert     pc1 == pc2
   assert not pc1 != pc2
   assert not pc1 <  pc2
   assert     pc1 <= pc2
   assert not pc1 >  pc2
   assert     pc1 >= pc2
