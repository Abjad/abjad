from abjad import *


def test_NumericPitch___cmp___01( ):

   p = pitchtools.NumericPitch(12)
   q = pitchtools.NumericPitch(13)

   assert     p <  q
   assert     p <= q
   assert not p == q
   assert     p != q
   assert not p >  q
   assert not p >= q


def test_NumericPitch___cmp___02( ):

   p = pitchtools.NumericPitch(12)
   q = pitchtools.NumericPitch(13)

   assert not q <  p
   assert not q <= p
   assert not q == p
   assert     q != p
   assert     q >  p
   assert     q >= p
