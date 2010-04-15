from abjad import *


def test_InversionIndicator___eq___01( ):

   t = tonalharmony.InversionIndicator(0)
   u = tonalharmony.InversionIndicator(0)
   v = tonalharmony.InversionIndicator(1)

   assert     t == t
   assert     t == u
   assert not t == v

   assert     u == t
   assert     u == u
   assert not u == v

   assert not v == t
   assert not v == u
   assert     v == v
