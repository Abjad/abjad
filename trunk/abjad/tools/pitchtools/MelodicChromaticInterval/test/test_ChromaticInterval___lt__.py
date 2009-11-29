from abjad import *


def test_ChromaticInterval___lt___01( ):
   '''Compare two ascending chromatic intervals.'''

   interval_1 = pitchtools.ChromaticInterval(2)
   interval_2 = pitchtools.ChromaticInterval(6)

   assert interval_1 < interval_2
   assert not interval_2 < interval_1


def test_ChromaticInterval___lt___02( ):
   '''Compare two descending chromatic intervals.'''

   interval_1 = pitchtools.ChromaticInterval(-2)
   interval_2 = pitchtools.ChromaticInterval(-6)

   assert interval_1 < interval_2
   assert not interval_2 < interval_1
