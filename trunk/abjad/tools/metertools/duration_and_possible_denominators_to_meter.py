from abjad.tools.metertools.Meter import Meter
from abjad.tools import mathtools
from abjad.tools import durtools


def duration_and_possible_denominators_to_meter(duration, denominators = None, factor = None):
   '''Return new Abjad Meter equal in duration to 'duration'.
   Determine meter denominator based on 'denominators' or 'factor'.
   Take denominator from smallest workable value in 'denominators'.
   Or take denominator from smallest workable multiple of 'factor'::

      abjad> metertools.duration_and_possible_denominators_to_meter(Rational(3, 2), [5, 6, 7, 8])
      metertools.Meter(9, 6)

   ::

      abjad> metertools.duration_and_possible_denominators_to_meter(Rational(3, 2), [4, 8, 16, 32])
      metertools.Meter(6, 4)

   ::

      abjad> metertools.duration_and_possible_denominators_to_meter(Rational(3, 2), factor = 5)
      metertools.Meter(15, 10)

   ::

      abjad> metertools.duration_and_possible_denominators_to_meter(Rational(3, 2))
      metertools.Meter(3, 2)

   .. versionchanged:: 1.1.2
      renamed ``metertools.make_best( )`` to
      ``metertools.duration_and_possible_denominators_to_meter( )``.
   '''

   if denominators is not None:
      if factor is not None:
         denominators = [d for d in denominators if factor in 
            mathtools.factors(d)]
      for desired_denominator in sorted(denominators):
         candidate_pair = durtools.rational_to_duration_pair_with_specified_integer_denominator(duration, desired_denominator)
         if candidate_pair[-1] == desired_denominator:
            return Meter(candidate_pair)

   if factor is not None:
      if factor in mathtools.factors(duration.denominator):
         return Meter(duration)
      else:
         meter_numerator = factor * duration.numerator
         meter_denominator = factor * duration.denominator
         return Meter(meter_numerator, meter_denominator)
   else:
      return Meter(duration)
