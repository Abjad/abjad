from abjad import *


def test_ExtentIndicator___eq___01( ):

   t = tonalharmony.ExtentIndicator(5)
   u = tonalharmony.ExtentIndicator(5)
   v = tonalharmony.ExtentIndicator(7)

   assert     t == t
   assert     t == u
   assert not t == v

   assert     u == t
   assert     u == u
   assert not u == v

   assert not v == t
   assert not v == u
   assert     v == v
