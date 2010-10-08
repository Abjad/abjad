from abjad import *


def test_NumericPitch___cmp___01( ):

   p = pitchtools.NumberedChromaticPitch(12)
   q = pitchtools.NumberedChromaticPitch(13)

   assert     p <  q
   assert     p <= q
   assert not p == q
   assert     p != q
   assert not p >  q
   assert not p >= q


def test_NumericPitch___cmp___02( ):

   p = pitchtools.NumberedChromaticPitch(12)
   q = pitchtools.NumberedChromaticPitch(13)

   assert not q <  p
   assert not q <= p
   assert not q == p
   assert     q != p
   assert     q >  p
   assert     q >= p
