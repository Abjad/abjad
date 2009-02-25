from abjad.helpers.in_terms_of import _in_terms_of
from abjad.meter.meter import Meter


def _make_best_meter(duration, denominators = None):
   '''Return new Abjad Meter, such that 

         1. meter duration equals 'duration', and
         2. meter denominator equals smallest feasible 
            element in 'denominators' list.

      _make_best_meter(Rational(3, 2), [5, 6, 7, 8])
      Meter(9, 6)

      _make_best_meter(Rational(3, 2), [4, 8, 16, 32])
      Meter(6, 4)

      _make_best_meter(Rational(3, 2))
      Meter(3, 2)'''

   if denominators is not None:
      for desired_denominator in sorted(denominators):
         candidate_pair = _in_terms_of(duration, desired_denominator)
         if candidate_pair[-1] == desired_denominator:
            return Meter(candidate_pair)

   return Meter(duration)
