from abjad import *


def test_ScaleDegree__init_by_symbolic_string_01( ):

   scale_degree = tonalharmony.ScaleDegree('I')
   assert scale_degree == tonalharmony.ScaleDegree(1)

   scale_degree = tonalharmony.ScaleDegree('i')
   assert scale_degree == tonalharmony.ScaleDegree(1)

   scale_degree = tonalharmony.ScaleDegree('bII')
   assert scale_degree == tonalharmony.ScaleDegree('flat', 2)

   scale_degree = tonalharmony.ScaleDegree('bii')
   assert scale_degree == tonalharmony.ScaleDegree('flat', 2)
