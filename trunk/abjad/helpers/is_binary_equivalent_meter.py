from abjad.tools import mathtools
from abjad.meter.meter import Meter
from abjad.rational.rational import Rational


def _is_binary_equivalent_meter(meter):
   '''True when meter is binary or when meter is nonbinary
      but mathematically equivalent to some binary meter,
      otherwise False.'''
   
   # check input
   assert isinstance(meter, Meter)

   # express meter as rational and reduce to relatively prime terms
   meter_as_rational = Rational(meter.numerator, meter.denominator)

   # return True if reduced meter denominator is power of two
   return mathtools.is_power_of_two(meter_as_rational._d)
