from abjad import *


def test_ScaleDegree_symbolic_string_01( ):

   assert tonalharmony.ScaleDegree(1).symbolic_string == 'I'
   assert tonalharmony.ScaleDegree('flat', 2).symbolic_string == 'bII'
   assert tonalharmony.ScaleDegree(3).symbolic_string == 'III'
   assert tonalharmony.ScaleDegree('sharp', 4).symbolic_string == '#IV'
   assert tonalharmony.ScaleDegree(5).symbolic_string == 'V'
   assert tonalharmony.ScaleDegree('flat', 6).symbolic_string == 'bVI'
   assert tonalharmony.ScaleDegree('flat', 7).symbolic_string == 'bVII'
