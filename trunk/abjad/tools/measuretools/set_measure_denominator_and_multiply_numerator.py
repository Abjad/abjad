from abjad.measure import _Measure
from abjad.meter import Meter
from abjad.tools import durtools


def set_measure_denominator_and_multiply_numerator(measure, denominator):
   r'''Set `measure` meter `denominator` and multiply
   meter numerator accordingly::

      abjad> measure = RigidMeasure((3, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
      abjad> Beam(measure.leaves)
      abjad> f(measure)
      {
         \time 3/8
         c'8 [
         d'8
         e'8 ]
      }
      
   ::
      
      abjad> measuretools.set_measure_denominator_and_multiply_numerator(measure, 16) 
      RigidMeasure(6/16, [c'8, d'8, e'8])
      
   ::
      
      abjad> f(measure)
      {
         \time 6/16
         c'8 [
         d'8
         e'8 ]
      }

   Leave `measure` contents unchanged.

   Return `measure`.
   '''



   if isinstance(measure, _Measure):
      ## to allow iteration inside zero-update loop
      forced_meter = measure.meter.forced
      if forced_meter is not None:
         old_meter = forced_meter
      else:
         old_meter = measure.meter.effective
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(old_meter_pair, denominator)
      measure.meter.forced = Meter(new_meter)

   return measure
