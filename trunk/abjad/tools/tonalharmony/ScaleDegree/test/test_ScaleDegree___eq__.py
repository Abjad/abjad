from abjad import *


def test_ScaleDegree___eq___01( ):

   t = tonalharmony.ScaleDegree(2)
   u = tonalharmony.ScaleDegree(2)
   v = tonalharmony.ScaleDegree(3)

   assert     t == t
   assert     t == u
   assert not t == v

   assert     u == t
   assert     u == u
   assert not u == v

   assert not v == t
   assert not v == u
   assert     v == v
