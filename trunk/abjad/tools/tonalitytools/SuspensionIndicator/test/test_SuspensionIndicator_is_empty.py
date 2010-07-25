from abjad import *


def test_SuspensionIndicator_is_empty_01( ):

   t = tonalitytools.SuspensionIndicator( )

   assert t.is_empty
