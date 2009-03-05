from abjad.helpers.container_contents_scale import container_contents_scale
from abjad.helpers.iterate import iterate
from abjad.helpers.leaf_duration_change import leaf_duration_change
from abjad.rational.rational import Rational
from abjad.tuplet.tuplet import _Tuplet


def measures_subsume(expr):
   r'''
      Subsume all measures in expr containing only top-level tuplet.
      Measures usually become nonbinary as as result of subsumption.

      Returns None because processes potentially many measures.

      t = RigidMeasure((2, 8), [FixedDurationTuplet((2, 8), scale(3))])
      measures_subsume(t)

      \time 3/12
      \scaleDurations #'(2 . 3) {
         c'8
         d'8
         e'8
      }
   '''

   for measure in iterate(expr, '_Measure'): 
      if len(measure) == 1:
         if isinstance(measure[0], _Tuplet):
            tuplet = measure[0]
            tuplet_multiplier = tuplet.duration.multiplier
            tuplet_denominator = tuplet_multiplier._d
            meter = measure.meter.effective
            meter_rational = Rational(meter.numerator, meter.denominator)
            numerator = meter_rational._n * tuplet_denominator
            denominator = meter_rational._d * tuplet_denominator
            measure.meter = (numerator, denominator)
            meter_multiplier = measure.meter.effective.multiplier
            written_adjustment = tuplet_multiplier / meter_multiplier
            measure[:] = tuplet[:]
            container_contents_scale(measure, written_adjustment)
