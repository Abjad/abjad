from abjad import *


def test_Meter_multiplier_01( ):
   t = metertools.Meter(7, 8)
   assert t.multiplier == Duration(1)

def test_Meter_multiplier_02( ):
   t = metertools.Meter(8, 8)
   assert t.multiplier == Duration(1)

def test_Meter_multiplier_03( ):
   t = metertools.Meter(8, 9)
   assert t.multiplier == Duration(8, 9)

def test_Meter_multiplier_04( ):
   t = metertools.Meter(9, 9)
   assert t.multiplier == Duration(8, 9)
