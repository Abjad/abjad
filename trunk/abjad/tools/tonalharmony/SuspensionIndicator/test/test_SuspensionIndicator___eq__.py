from abjad import *


def test_SuspensionIndicator___eq___01( ):

   t = tonalharmony.SuspensionIndicator(4, 3)
   u = tonalharmony.SuspensionIndicator(4, 3)
   v = tonalharmony.SuspensionIndicator(2, 1)

   assert     t == t
   assert     t == u
   assert not t == v

   assert     u == t
   assert     u == u
   assert not u == v

   assert not v == t
   assert not v == u
   assert     v == v
