from abjad import *


def test_SuspensionIndicator__init_empty_01( ):

   t = tonalitytools.SuspensionIndicator( )

   assert t.start is None
   assert t.stop is None
