from abjad import *


def test_meter_eq_01( ):
   '''
   Meters evaluate eq to True when numerators and denominators match.
   '''

   assert Meter(3, 8) == Meter(3, 8)


def test_meter_eq_02( ):
   '''
   Meters evaluate eq to False when meters match only numerically.
   '''

   assert not Meter(3, 8) == Meter(6, 16)
