from abjad import *


def test_SuspensionIndicator__init_by_stop_and_start_01( ):

   t = tonalharmony.SuspensionIndicator(4, 3)

   assert t.start == tonalharmony.ScaleDegree(4)
   assert t.stop == tonalharmony.ScaleDegree(3)


def test_SuspensionIndicator__init_by_stop_and_start_02( ):

   t = tonalharmony.SuspensionIndicator(4, ('flat', 3))

   assert t.start == tonalharmony.ScaleDegree(4)
   assert t.stop == tonalharmony.ScaleDegree('flat', 3)
