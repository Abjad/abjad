from abjad import *


def test_SuspensionIndicator__init_by_reference_01( ):

   t = tonalharmony.SuspensionIndicator(4, 3)
   u = tonalharmony.SuspensionIndicator(t)

   assert t is not u
   assert t == u
