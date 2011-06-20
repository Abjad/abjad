from abjad import *
from abjad.tools import metertools


def test_metertools_is_meter_with_equivalent_binary_representation_01( ):
   '''True when meter is binary or when meter is nonbinary
      but mathematically equivalent to some binary meter.'''

   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(1, 12))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(2, 12))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(3, 12))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(4, 12))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(5, 12))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(6, 12))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(7, 12))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(8, 12))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(9, 12))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(10, 12))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(11, 12))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(12, 12))
      

def test_metertools_is_meter_with_equivalent_binary_representation_02( ):
   '''True when meter is binary or when meter is nonbinary
      but mathematically equivalent to some binary meter.'''

   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(1, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(2, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(3, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(4, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(5, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(6, 14))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(7, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(8, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(9, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(10, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(11, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(12, 14))
   assert not metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(13, 14))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(14, 14))


def test_metertools_is_meter_with_equivalent_binary_representation_03( ):
   '''True for binary meters.'''

   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(1, 8))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(2, 8))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(3, 8))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(4, 8))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(5, 8))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(6, 8))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(7, 8))
   assert metertools.is_meter_with_equivalent_binary_representation(metertools.Meter(8, 8))
