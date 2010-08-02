from abjad import *


def test_meter_nonzero_01( ):
   '''
   All Abjad meters evaluate to True.
   '''

   assert Meter(3, 8)


def test_meter_nonzero_02( ):
   '''
   All Abjad meters evaluate to True.
   '''

   assert Meter(0, 1)
