from abjad.tools import componenttools
from abjad.tools import iterate
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.components._Tuplet import FixedDurationTuplet


def move_measure_prolation_to_full_measure_tuplet(expr):
   '''Turn nonbinary measures into binary measures 
   containing a single fixed-duration tuplet.

   This is the inverse of measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure( ).

   Note that not all nonbinary measures can be made binary.

   Returns None because processes potentially many measures.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.project( )`` to
      ``measuretools.move_measure_prolation_to_full_measure_tuplet( )``.
   '''

   from abjad.tools import containertools
   for measure in iterate.measures_forward_in_expr(expr):
      if measure.meter.effective.nonbinary:

         # find meter and contents multipliers
         meter_multiplier = measure.meter.effective.multiplier
         contents_multiplier = componenttools.get_likely_multiplier_of_components(measure[:])

         # update nonbinary meter to binary
         metertools.meter_to_binary_meter(measure.meter.effective, contents_multiplier)

         # find target duration and create tuplet
         target_duration = meter_multiplier * measure.duration.contents
         tuplet = FixedDurationTuplet(target_duration, measure[:])

         # scale tuplet contents, if helpful
         if contents_multiplier is not None:
            containertools.scale_contents_of_container(
               tuplet, ~contents_multiplier)
