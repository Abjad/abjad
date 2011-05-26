from fractions import Fraction
from abjad.tools import durtools
from abjad.tools import contexttools
from abjad.tools import metertools
from abjad.tools.measuretools.scale_contents_of_measures_in_expr import scale_contents_of_measures_in_expr


def scale_measure_denominator_and_adjust_measure_contents(measure, new_denominator_factor):
   r'''.. versionadded:: 1.1.1

   Change binary `measure` to nonbinary measure
   with `new_denominator_factor`::

      abjad> measure = Measure((2, 8), macros.scale(2))
      abjad> spannertools.BeamSpanner(measure.leaves)
      abjad> f(measure)
      {
         \time 2/8
         c'8 [
         d'8 ]
      }
      
   ::
      
      abjad> measuretools.scale_measure_denominator_and_adjust_measure_contents(measure, 3)
      Measure(3/12, [c'8., d'8.])
      
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

   .. versionchanged:: 1.1.2
      renamed ``measuretools.change_binary_measure_to_nonbinary( )`` to
      ``measuretools.scale_measure_denominator_and_adjust_measure_contents( )``.
   '''

   ## save old meter duration
   old_meter_duration = contexttools.get_effective_time_signature(measure).duration

   ## find new meter
   new_meter = metertools.duration_and_possible_denominators_to_meter(
      old_meter_duration, factor = new_denominator_factor)

   ## find new measure multiplier
   new_measure_multiplier = durtools.positive_integer_to_implied_prolation_multipler(
      new_denominator_factor) 

   ## inverse scale measure ... but throw away resultant meter
   numerator, denominator = new_measure_multiplier.numerator, new_measure_multiplier.denominator
   inverse_measure_multiplier = Fraction(denominator, numerator)
   scale_contents_of_measures_in_expr(measure, inverse_measure_multiplier)

   ## assign new meter
   measure._attach_explicit_meter(new_meter)

   ## return measure
   return measure
