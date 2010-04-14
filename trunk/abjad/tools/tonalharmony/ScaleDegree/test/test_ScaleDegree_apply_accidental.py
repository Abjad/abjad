from abjad import *


def test_ScaleDegree_apply_accidental_01( ):

   degree = tonalharmony.ScaleDegree('flat', 2)
   assert degree.apply_accidental('sharp') == tonalharmony.ScaleDegree(2)
   assert degree.apply_accidental('ss') == tonalharmony.ScaleDegree('sharp', 2)
