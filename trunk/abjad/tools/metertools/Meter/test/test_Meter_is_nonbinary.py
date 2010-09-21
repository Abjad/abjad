from abjad import *


def test_Meter_is_nonbinary_01( ):
   t = metertools.Meter(7, 8)
   assert t.is_nonbinary == False

def test_Meter_is_nonbinary_02( ):
   t = metertools.Meter(8, 8)
   assert t.is_nonbinary == False

def test_Meter_is_nonbinary_03( ):
   t = metertools.Meter(8, 9)
   assert t.is_nonbinary == True

def test_Meter_is_nonbinary_04( ):
   t = metertools.Meter(9, 9)
   assert t.is_nonbinary == True
