from abjad.meter import Meter
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import mathtools


def make_binary(nonbinary_meter, contents_multiplier = Rational(1)):
   '''Change nonbinary meter to binary.
      Return meter.

      metertools.make_binary(Meter(3, 12))
      Meter(2, 8)'''
   
   # check input
   assert isinstance(nonbinary_meter, Meter)
   assert isinstance(contents_multiplier, Rational)

   # save nonbinary meter and denominator
   nonbinary_denominator = nonbinary_meter.denominator

   # find binary denominator
   if contents_multiplier == Rational(1):
      binary_denominator = mathtools.greatest_power_of_two_less_equal(
         nonbinary_denominator)
   else:
      binary_denominator = mathtools.greatest_power_of_two_less_equal(
         nonbinary_denominator, 1)

   # find binary pair
   nonbinary_pair = (nonbinary_meter.numerator, nonbinary_meter.denominator)
   binary_pair = durtools.in_terms_of(nonbinary_pair, binary_denominator)

   # update meter numerator and denominator
   nonbinary_meter.numerator = binary_pair[0]
   nonbinary_meter.denominator = binary_pair[1]

   # return meter
   return nonbinary_meter
