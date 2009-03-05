from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.helpers.iterate import iterate
from abjad.helpers.meter_make_binary import meter_make_binary
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def measures_project(expr):
   '''Turn nonbinary measures into binary measures 
      containing a single fixed-duration tuplet.

      This is the inverse of measures_subsume( ).

      Note that not all nonbinary measures can be made binary.

      Returns None because processes potentially many measures.

      TODO: add keyword to allow fixed-multiplier tuplet.'''

   for measure in iterate(expr, '_Measure'):
      if measure.meter.effective.nonbinary:
         multiplier = measure.meter.effective.multiplier
         meter_make_binary(measure.meter.effective)
         target_duration = multiplier * measure.duration.contents
         FixedDurationTuplet(target_duration, measure[:])
