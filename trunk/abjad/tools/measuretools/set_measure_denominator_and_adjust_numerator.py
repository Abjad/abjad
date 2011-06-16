from abjad.tools.measuretools.Measure import Measure
from abjad.tools import contexttools
from abjad.tools import durtools
from abjad.tools.metertools import Meter


def set_measure_denominator_and_adjust_numerator(measure, denominator):
   r'''Set `measure` meter `denominator` and multiply
   meter numerator accordingly::

      abjad> measure = Measure((3, 8), "c'8 d'8 e'8")
      abjad> spannertools.BeamSpanner(measure.leaves)
      BeamSpanner(c'8, d'8, e'8)
      abjad> f(measure)
      {
         \time 3/8
         c'8 [
         d'8
         e'8 ]
      }
      
   ::
      
      abjad> measuretools.set_measure_denominator_and_adjust_numerator(measure, 16) 
      Measure(6/16, [c'8, d'8, e'8])
      
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

   .. todo::
      implement ``measuretools.set_measure_denominator_and_adjust_contents( )``.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.set_measure_denominator_and_multiply_numerator( )`` to
      ``measuretools.set_measure_denominator_and_adjust_numerator( )``.
   '''



   if isinstance(measure, Measure):
      ## to allow iteration inside zero-update loop
      forced_meter = measure._explicit_meter
      if forced_meter is not None:
         old_meter = forced_meter
      else:
         old_meter = contexttools.get_effective_time_signature(measure)
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(
         old_meter_pair, denominator)
      measure._attach_explicit_meter(*new_meter)

   return measure
