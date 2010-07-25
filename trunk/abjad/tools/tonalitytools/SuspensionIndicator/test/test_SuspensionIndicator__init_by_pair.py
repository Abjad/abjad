from abjad import *


def test_SuspensionIndicator__init_by_pair_01( ):

   t = tonalitytools.SuspensionIndicator((4, 3))

   assert t.start == tonalitytools.ScaleDegree(4)
   assert t.stop == tonalitytools.ScaleDegree(3) 
