from abjad import *


def test_NumericPitch___eq___01( ):

   p = pitchtools.NumericPitch(12)
   q = pitchtools.NumericPitch(12)
   r = pitchtools.NumericPitch(13)

   assert p == p
   assert p == q
   assert not p == r
   
   assert q == p
   assert q == q
   assert not q == r
   
   assert not r == p
   assert not r == q
   assert r == r
