from abjad import *


def test_ScaleDegree___str___01( ):

   assert str(tonalharmony.ScaleDegree(1)) == '1'
   assert str(tonalharmony.ScaleDegree('flat', 2)) == 'b2'
   assert str(tonalharmony.ScaleDegree('sharp', 4)) == '#4'
