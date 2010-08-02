from abjad import *


def test_Meter_multiplier_01( ):
   t = Meter(7, 8)
   assert t.multiplier == Rational(1)

def test_Meter_multiplier_02( ):
   t = Meter(8, 8)
   assert t.multiplier == Rational(1)

def test_Meter_multiplier_03( ):
   t = Meter(8, 9)
   assert t.multiplier == Rational(8, 9)

def test_Meter_multiplier_04( ):
   t = Meter(9, 9)
   assert t.multiplier == Rational(8, 9)
