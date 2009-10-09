from abjad import *


def test_pitchtools_PC___cmp___01( ):
   '''All six comparison operators work as expected
   on different-valued PCs.'''

   pc1 = pitchtools.PC(6)
   pc2 = pitchtools.PC(7)

   assert not pc1 == pc2
   assert     pc1 != pc2
   assert     pc1 <  pc2
   assert     pc1 <= pc2
   assert not pc1 >  pc2
   assert not pc1 >= pc2


def test_pitchtools_PC___cmp___02( ):
   '''All six comparison operators work as expected
   on same-valued PCs.'''

   pc1 = pitchtools.PC(6)
   pc2 = pitchtools.PC(6)

   assert     pc1 == pc2
   assert not pc1 != pc2
   assert not pc1 <  pc2
   assert     pc1 <= pc2
   assert not pc1 >  pc2
   assert     pc1 >= pc2
