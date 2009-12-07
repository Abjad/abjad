from abjad import *


def test_PitchClass___cmp___01( ):
   '''All six comparison operators work as expected
   on different-valued pitch classes.'''

   pc1 = pitchtools.PitchClass(6)
   pc2 = pitchtools.PitchClass(7)

   assert not pc1 == pc2
   assert     pc1 != pc2
   assert     pc1 <  pc2
   assert     pc1 <= pc2
   assert not pc1 >  pc2
   assert not pc1 >= pc2


def test_PitchClass___cmp___02( ):
   '''All six comparison operators work as expected
   on same-valued PitchClasss.'''

   pc1 = pitchtools.PitchClass(6)
   pc2 = pitchtools.PitchClass(6)

   assert     pc1 == pc2
   assert not pc1 != pc2
   assert not pc1 <  pc2
   assert     pc1 <= pc2
   assert not pc1 >  pc2
   assert     pc1 >= pc2
