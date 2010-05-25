from abjad import *


def test_SuspensionIndicator__init_by_start_and_stop_01( ):

   t = tonalharmony.SuspensionIndicator(4, 3)

   assert t.start == tonalharmony.ScaleDegree(4)
   assert t.stop == tonalharmony.ScaleDegree(3)


def test_SuspensionIndicator__init_by_start_and_stop_02( ):

   t = tonalharmony.SuspensionIndicator(4, ('flat', 3))

   assert t.start == tonalharmony.ScaleDegree(4)
   assert t.stop == tonalharmony.ScaleDegree('flat', 3)
