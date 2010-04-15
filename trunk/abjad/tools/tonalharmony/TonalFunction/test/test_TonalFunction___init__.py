from abjad import *


def test_TonalFunction___init___01( ):

   harmony = tonalharmony.TonalFunction(5, 'dominant', 7, 0)

   assert harmony.scale_degree == tonalharmony.ScaleDegree(5)
   assert harmony.quality == tonalharmony.QualityIndicator('dominant')
   assert harmony.extent == tonalharmony.ExtentIndicator(7)
   assert harmony.inversion == tonalharmony.InversionIndicator('root position')


def test_TonalFunction___init___02( ):

   harmony = tonalharmony.TonalFunction(('flat', 2), 'major', 5, 1)

   assert harmony.scale_degree == tonalharmony.ScaleDegree('flat', 2)
   assert harmony.quality == tonalharmony.QualityIndicator('major')
   assert harmony.extent == tonalharmony.ExtentIndicator(5)
   assert harmony.inversion == tonalharmony.InversionIndicator('first')
