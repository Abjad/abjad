from abjad.tools import durtools
from abjad.tools import metertools
from abjad.tools.measuretools.scale import scale as measuretools_scale


def change_binary_measure_to_nonbinary(measure, new_denominator_factor):
   r'''.. versionadded:: 1.1.1

   Change binary `measure` to nonbinary measure
   with `new_denominator_factor`::

      abjad> measure = RigidMeasure((2, 8), construct.scale(2))
      abjad> Beam(measure.leaves)
      abjad> f(measure)
      {
         \time 2/8
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> measuretools.change_binary_measure_to_nonbinary(measure, 3)
      RigidMeasure(3/12, [c'8., d'8.])
      
   ::
      
      abjad> f(measure)
      {
         \time 3/12
         \scaleDurations #'(2 . 3) {
            c'8. [
            d'8. ]
         }
      }


   Treat `new_denominator_factor` like clever form of ``1``:
   ``3/3`` or ``5/5`` or ``7/7``, etc.

   Preserve `measure` prolated duration.

   Derive new `measure` multiplier.

   Scale `measure` contents.

   Pick best new meter.

   .. todo:: implement ``measuretools.change_nonbinary_measure_to_binary( )``.
   '''

   ## save old meter duration
   old_meter_duration = measure.meter.effective.duration

   ## find new meter
   new_meter = metertools.make_best(
      old_meter_duration, factor = new_denominator_factor)

   ## find new measure multiplier
   new_measure_multiplier = durtools.denominator_to_multiplier(
      new_denominator_factor) 

   ## inverse scale measure ... but throw away resultant meter
   measuretools_scale(measure, ~new_measure_multiplier)

   ## assign new meter
   measure.meter.forced = new_meter

   ## return measure
   return measure
