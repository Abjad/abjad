from abjad.Meter import Meter
from abjad.tools import mathtools


def get_nonbinary_factor_from_meter_denominator(meter):
   '''Return nonbinary factor in denominator of meter, else 1.'''

   assert isinstance(meter, Meter)
   nonbinary_factor = mathtools.remove_powers_of_two(meter.denominator)
   return nonbinary_factor
