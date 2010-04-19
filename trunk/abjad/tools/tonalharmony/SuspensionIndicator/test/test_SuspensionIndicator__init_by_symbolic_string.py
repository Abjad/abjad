from abjad import *


def test_SuspensionIndicator__init_by_symbolic_string_01( ):

   t = tonalharmony.SuspensionIndicator('4-3')
   assert t.start == tonalharmony.ScaleDegree(4)
   assert t.stop == tonalharmony.ScaleDegree(3)

   t = tonalharmony.SuspensionIndicator('b2-1')
   assert t.start == tonalharmony.ScaleDegree('flat', 2)
   assert t.stop == tonalharmony.ScaleDegree(1)
