from abjad import *


def test_SuspensionIndicator__init_by_pair_01( ):

   t = tonalharmony.SuspensionIndicator((4, 3))

   assert t.start == tonalharmony.ScaleDegree(4)
   assert t.stop == tonalharmony.ScaleDegree(3) 
