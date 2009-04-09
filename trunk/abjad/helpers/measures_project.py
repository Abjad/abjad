from abjad.helpers.components_likely_multiplier import \
   _components_likely_multiplier
from abjad.helpers.container_scale import container_scale
from abjad.tools import mathtools
from abjad.tools import mathtools
from abjad.tools import iterate
from abjad.tools import metertools
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def measures_project(expr):
   '''Turn nonbinary measures into binary measures 
      containing a single fixed-duration tuplet.

      This is the inverse of measures_subsume( ).

      Note that not all nonbinary measures can be made binary.

      Returns None because processes potentially many measures.'''

   from abjad.measure.measure import _Measure
   for measure in iterate.naive(expr, _Measure):
      if measure.meter.effective.nonbinary:

         # find meter and contents multipliers
         meter_multiplier = measure.meter.effective.multiplier
         contents_multiplier = _components_likely_multiplier(measure[:])

         # update nonbinary meter to binary
         metertools.make_binary(measure.meter.effective, contents_multiplier)

         # find target duration and create tuplet
         target_duration = meter_multiplier * measure.duration.contents
         tuplet = FixedDurationTuplet(target_duration, measure[:])

         # scale tuplet contents, if helpful
         if contents_multiplier is not None:
            container_scale(tuplet, ~contents_multiplier)
