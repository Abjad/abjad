from abjad import *


def test_QualityIndicator___eq___01( ):

   t = tonalharmony.QualityIndicator('major')
   u = tonalharmony.QualityIndicator('major')
   v = tonalharmony.QualityIndicator('minor')

   assert     t == t
   assert     t == u
   assert not t == v

   assert     u == t
   assert     u == u
   assert not u == v

   assert not v == t
   assert not v == u
   assert     v == v
