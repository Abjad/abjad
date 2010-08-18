from abjad import *


def test_metertools_meter_to_binary_meter_01( ):
   '''Make n/12 meters into n/8 meters, where possible.'''

   assert metertools.meter_to_binary_meter(metertools.Meter(1, 12)) == metertools.Meter(1, 12)
   assert metertools.meter_to_binary_meter(metertools.Meter(2, 12)) == metertools.Meter(2, 12)
   assert metertools.meter_to_binary_meter(metertools.Meter(3, 12)) == metertools.Meter(2, 8)
   assert metertools.meter_to_binary_meter(metertools.Meter(4, 12)) == metertools.Meter(4, 12)
   assert metertools.meter_to_binary_meter(metertools.Meter(5, 12)) == metertools.Meter(5, 12)
   assert metertools.meter_to_binary_meter(metertools.Meter(6, 12)) == metertools.Meter(4, 8)


def test_metertools_meter_to_binary_meter_02( ):
   '''Make n/14 meters into n/8 meters, where possible.'''

   assert metertools.meter_to_binary_meter(metertools.Meter(1, 14)) == metertools.Meter(1, 14)
   assert metertools.meter_to_binary_meter(metertools.Meter(2, 14)) == metertools.Meter(2, 14)
   assert metertools.meter_to_binary_meter(metertools.Meter(3, 14)) == metertools.Meter(3, 14)
   assert metertools.meter_to_binary_meter(metertools.Meter(4, 14)) == metertools.Meter(4, 14)
   assert metertools.meter_to_binary_meter(metertools.Meter(5, 14)) == metertools.Meter(5, 14)
   assert metertools.meter_to_binary_meter(metertools.Meter(6, 14)) == metertools.Meter(6, 14)
   assert metertools.meter_to_binary_meter(metertools.Meter(7, 14)) == metertools.Meter(4, 8)


def test_metertools_meter_to_binary_meter_03( ):
   '''Make n/24 meters into n/16 meters, where possible.'''

   assert metertools.meter_to_binary_meter(metertools.Meter(1, 24)) == metertools.Meter(1, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(2, 24)) == metertools.Meter(2, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(3, 24)) == metertools.Meter(2, 16)
   assert metertools.meter_to_binary_meter(metertools.Meter(4, 24)) == metertools.Meter(4, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(5, 24)) == metertools.Meter(5, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(6, 24)) == metertools.Meter(4, 16)
   assert metertools.meter_to_binary_meter(metertools.Meter(7, 24)) == metertools.Meter(7, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(8, 24)) == metertools.Meter(8, 24)


def test_metertools_meter_to_binary_meter_04( ):
   '''Make n/24 meters into n/8 meters, where possible.'''

   assert metertools.meter_to_binary_meter(metertools.Meter(1, 24), Rational(99)) == metertools.Meter(1, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(2, 24), Rational(99)) == metertools.Meter(2, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(3, 24), Rational(99)) == metertools.Meter(1, 8)
   assert metertools.meter_to_binary_meter(metertools.Meter(4, 24), Rational(99)) == metertools.Meter(4, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(5, 24), Rational(99)) == metertools.Meter(5, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(6, 24), Rational(99)) == metertools.Meter(2, 8)
   assert metertools.meter_to_binary_meter(metertools.Meter(7, 24), Rational(99)) == metertools.Meter(7, 24)
   assert metertools.meter_to_binary_meter(metertools.Meter(8, 24), Rational(99)) == metertools.Meter(8, 24)
