from abjad import *


def test_ScaleDegree__init_by_pair_01( ):

   degree = tonalharmony.ScaleDegree(('flat', 2))

   assert degree.accidental == pitchtools.Accidental('flat')
   assert degree.number == 2
