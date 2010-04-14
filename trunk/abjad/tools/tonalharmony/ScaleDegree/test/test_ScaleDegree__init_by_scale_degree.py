from abjad import *


def test_ScaleDegree__init_by_scale_degree_01( ):

   degree = tonalharmony.ScaleDegree('flat', 2)
   new = tonalharmony.ScaleDegree(degree)

   assert new is not degree
   assert new.accidental == pitchtools.Accidental('flat')
   assert new.number == 2
