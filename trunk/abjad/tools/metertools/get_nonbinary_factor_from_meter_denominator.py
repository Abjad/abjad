from abjad.tools import mathtools
from abjad.tools.metertools.Meter import Meter


def get_nonbinary_factor_from_meter_denominator(meter):
   '''Get nonbinary factor from nonbinary `meter` denominator::

      abjad> metertools.get_nonbinary_factor_from_meter_denominator(metertools.Meter(3, 12))
      3

   ::

      abjad> metertools.get_nonbinary_factor_from_meter_denominator(metertools.Meter(3, 13))
      13

   ::

      abjad> metertools.get_nonbinary_factor_from_meter_denominator(metertools.Meter(3, 14))
      7

   ::

      abjad> metertools.get_nonbinary_factor_from_meter_denominator(metertools.Meter(3, 15))
      15

   Get ``1`` from binary `meter` denominator::

      abjad> metertools.get_nonbinary_factor_from_meter_denominator(metertools.Meter(3, 16))
      1

   Return nonnegative integer.
   '''

   ## check input
   assert isinstance(meter, Meter)

   ## get nonbinary factor from meter denominator
   nonbinary_factor = mathtools.remove_powers_of_two(meter.denominator)

   ## return nonbinary factor
   return nonbinary_factor
