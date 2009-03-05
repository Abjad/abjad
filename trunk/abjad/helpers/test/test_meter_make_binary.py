from abjad import *


def test_meter_make_binary_01( ):
   '''Make n/12 meters into n/8 meters, where possible.'''

   assert meter_make_binary(Meter(1, 12)) == Meter(1, 12)
   assert meter_make_binary(Meter(2, 12)) == Meter(2, 12)
   assert meter_make_binary(Meter(3, 12)) == Meter(2, 8)
   assert meter_make_binary(Meter(4, 12)) == Meter(4, 12)
   assert meter_make_binary(Meter(5, 12)) == Meter(5, 12)
   assert meter_make_binary(Meter(6, 12)) == Meter(4, 8)


def test_meter_make_binary_02( ):
   '''Make n/14 meters into n/8 meters, where possible.'''

   assert meter_make_binary(Meter(1, 14)) == Meter(1, 14)
   assert meter_make_binary(Meter(2, 14)) == Meter(2, 14)
   assert meter_make_binary(Meter(3, 14)) == Meter(3, 14)
   assert meter_make_binary(Meter(4, 14)) == Meter(4, 14)
   assert meter_make_binary(Meter(5, 14)) == Meter(5, 14)
   assert meter_make_binary(Meter(6, 14)) == Meter(6, 14)
   assert meter_make_binary(Meter(7, 14)) == Meter(4, 8)
