from abjad import *


def test_SuspensionIndicator__init_by_reference_01( ):

   t = tonalitytools.SuspensionIndicator(4, 3)
   u = tonalitytools.SuspensionIndicator(t)

   assert t is not u
   assert t == u
