from abjad import *


def test_TonalFunction_suspension_01( ):

   t = tonalharmony.TonalFunction(5, 'major', 5, 0, (4, 3))

   assert t.suspension == tonalharmony.SuspensionIndicator(4, 3)
   assert t.suspension.start == tonalharmony.ScaleDegree(4)
   assert t.suspension.stop == tonalharmony.ScaleDegree(3)
