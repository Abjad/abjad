from abjad import *
from abjad.helpers.is_binary_equivalent_meter import _is_binary_equivalent_meter


def test_is_binary_equivalent_meter_01( ):
   '''True when meter is binary or when meter is nonbinary
      but mathematically equivalent to some binary meter.'''

   assert not _is_binary_equivalent_meter(Meter(1, 12))
   assert not _is_binary_equivalent_meter(Meter(2, 12))
   assert _is_binary_equivalent_meter(Meter(3, 12))
   assert not _is_binary_equivalent_meter(Meter(4, 12))
   assert not _is_binary_equivalent_meter(Meter(5, 12))
   assert _is_binary_equivalent_meter(Meter(6, 12))
   assert not _is_binary_equivalent_meter(Meter(7, 12))
   assert not _is_binary_equivalent_meter(Meter(8, 12))
   assert _is_binary_equivalent_meter(Meter(9, 12))
   assert not _is_binary_equivalent_meter(Meter(10, 12))
   assert not _is_binary_equivalent_meter(Meter(11, 12))
   assert _is_binary_equivalent_meter(Meter(12, 12))
      

def test_is_binary_equivalent_meter_02( ):
   '''True when meter is binary or when meter is nonbinary
      but mathematically equivalent to some binary meter.'''

   assert not _is_binary_equivalent_meter(Meter(1, 14))
   assert not _is_binary_equivalent_meter(Meter(2, 14))
   assert not _is_binary_equivalent_meter(Meter(3, 14))
   assert not _is_binary_equivalent_meter(Meter(4, 14))
   assert not _is_binary_equivalent_meter(Meter(5, 14))
   assert not _is_binary_equivalent_meter(Meter(6, 14))
   assert _is_binary_equivalent_meter(Meter(7, 14))
   assert not _is_binary_equivalent_meter(Meter(8, 14))
   assert not _is_binary_equivalent_meter(Meter(9, 14))
   assert not _is_binary_equivalent_meter(Meter(10, 14))
   assert not _is_binary_equivalent_meter(Meter(11, 14))
   assert not _is_binary_equivalent_meter(Meter(12, 14))
   assert not _is_binary_equivalent_meter(Meter(13, 14))
   assert _is_binary_equivalent_meter(Meter(14, 14))


def test_is_binary_equivalent_meter_03( ):
   '''True for binary meters.'''

   assert _is_binary_equivalent_meter(Meter(1, 8))
   assert _is_binary_equivalent_meter(Meter(2, 8))
   assert _is_binary_equivalent_meter(Meter(3, 8))
   assert _is_binary_equivalent_meter(Meter(4, 8))
   assert _is_binary_equivalent_meter(Meter(5, 8))
   assert _is_binary_equivalent_meter(Meter(6, 8))
   assert _is_binary_equivalent_meter(Meter(7, 8))
   assert _is_binary_equivalent_meter(Meter(8, 8))
