from abjad.tools.metertools.Meter import Meter
from fractions import Fraction
from abjad.tools import mathtools


def is_meter_with_equivalent_binary_representation(meter):
   '''True when meter is binary or when meter is nonbinary
      but mathematically equivalent to some binary meter,
      otherwise False.
   '''
   
   # check input
   assert isinstance(meter, Meter)

   # express meter as rational and reduce to relatively prime terms
   meter_as_rational = Fraction(meter.numerator, meter.denominator)

   # return True if reduced meter denominator is power of two
   return mathtools.is_power_of_two(meter_as_rational.denominator)
