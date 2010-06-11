from abjad.tools import componenttools
from abjad.tools import iterate
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.tuplet import FixedDurationTuplet


def project(expr):
   '''Turn nonbinary measures into binary measures 
   containing a single fixed-duration tuplet.

   This is the inverse of measuretools.subsume( ).

   Note that not all nonbinary measures can be made binary.

   Returns None because processes potentially many measures.
   '''

   from abjad.tools import containertools
   for measure in iterate.measures_forward_in(expr):
      if measure.meter.effective.nonbinary:

         # find meter and contents multipliers
         meter_multiplier = measure.meter.effective.multiplier
         contents_multiplier = componenttools.get_likely_multiplier(measure[:])

         # update nonbinary meter to binary
         metertools.meter_to_binary_meter(measure.meter.effective, contents_multiplier)

         # find target duration and create tuplet
         target_duration = meter_multiplier * measure.duration.contents
         tuplet = FixedDurationTuplet(target_duration, measure[:])

         # scale tuplet contents, if helpful
         if contents_multiplier is not None:
            containertools.scale_container_contents(
               tuplet, ~contents_multiplier)
