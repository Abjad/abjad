from abjad import *


def test_TonalFunction_bass_scale_degree_01( ):

   t = tonalharmony.TonalFunction(5, 'major', 5, 0)
   assert t.bass_scale_degree == tonalharmony.ScaleDegree(5)

   t = tonalharmony.TonalFunction(5, 'major', 5, 1)
   assert t.bass_scale_degree == tonalharmony.ScaleDegree(7)

   t = tonalharmony.TonalFunction(5, 'major', 5, 2)
   assert t.bass_scale_degree == tonalharmony.ScaleDegree(2)


def test_TonalFunction_bass_scale_degree_02( ):

   t = tonalharmony.TonalFunction(5, 'major', 7, 0)
   assert t.bass_scale_degree == tonalharmony.ScaleDegree(5)

   t = tonalharmony.TonalFunction(5, 'major', 7, 1)
   assert t.bass_scale_degree == tonalharmony.ScaleDegree(7)

   t = tonalharmony.TonalFunction(5, 'major', 7, 2)
   assert t.bass_scale_degree == tonalharmony.ScaleDegree(2)

   t = tonalharmony.TonalFunction(5, 'major', 7, 3)
   assert t.bass_scale_degree == tonalharmony.ScaleDegree(4)
