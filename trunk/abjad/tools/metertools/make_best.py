from abjad.meter.meter import Meter
#from abjad.tools import mathtools as mt
from abjad.tools import mathtools
from abjad.tools import durtools


def make_best(duration, denominators = None, factor = None):
   '''Return new Abjad Meter, such that 

         1. meter duration equals 'duration', and
         2. meter denominator equals smallest feasible 
            element in 'denominators' list.

      metertools.make_best(Rational(3, 2), [5, 6, 7, 8])
      Meter(9, 6)

      metertools.make_best(Rational(3, 2), [4, 8, 16, 32])
      Meter(6, 4)

      metertools.make_best(Rational(3, 2))
      Meter(3, 2)'''

   if denominators is not None:
      if factor is not None:
         #denominators = [d for d in denominators if factor in mt.factors(d)]
         denominators = [d for d in denominators if factor in mathtools.factors(d)]
      for desired_denominator in sorted(denominators):
         candidate_pair = durtools.in_terms_of(duration, desired_denominator)
         if candidate_pair[-1] == desired_denominator:
            return Meter(candidate_pair)

   if factor is not None:
      #if factor in mt.factors(duration._d):
      if factor in mathtools.factors(duration._d):
         return Meter(duration)
      else:
         meter_numerator = factor * duration._n
         meter_denominator = factor * duration._d
         return Meter(meter_numerator, meter_denominator)
   else:
      return Meter(duration)
