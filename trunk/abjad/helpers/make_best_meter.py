from abjad.helpers.in_terms_of import _in_terms_of
from abjad.meter.meter import Meter


def _make_best_meter(duration, denominators = None):
   '''Return new Abjad meter equal to duration and
      with denominator equal to the smallest feasible
      integer in denominator_list.

      TODO: Write tests.
   
      TODO: Make work with multielement denominators list.

      TODO: Make work with empty denominators list.'''

   new_pair = _in_terms_of(duration, min(denominators))
   if new_pair[1] != min(denominators):
      new_pair = _in_terms_of(new_pair, max(denominators))
   new_meter = Meter(new_pair)
   return new_meter
