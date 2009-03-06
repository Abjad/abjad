from abjad.helpers.components_likely_multiplier import _components_likely_multiplier
from abjad.helpers.container_contents_scale import container_contents_scale
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

         # find meter and contents multipliers
         meter_multiplier = measure.meter.effective.multiplier
         contents_multiplier = _components_likely_multiplier(measure[:])

         # update nonbinary meter to binary
         meter_make_binary(measure.meter.effective, contents_multiplier)

         # find target duration and create tuplet
         target_duration = meter_multiplier * measure.duration.contents
         tuplet = FixedDurationTuplet(target_duration, measure[:])

         # scale tuplet contents, if helpful
         if contents_multiplier is not None:
            container_contents_scale(tuplet, ~contents_multiplier)
