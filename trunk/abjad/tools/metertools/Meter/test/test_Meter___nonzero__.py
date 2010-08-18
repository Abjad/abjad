from abjad import *


def test_Meter___nonzero___01( ):
   '''
   All Abjad meters evaluate to True.
   '''

   assert metertools.Meter(3, 8)


def test_Meter___nonzero___02( ):
   '''
   All Abjad meters evaluate to True.
   '''

   assert metertools.Meter(0, 1)
