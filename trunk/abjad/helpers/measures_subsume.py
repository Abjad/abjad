#from abjad.helpers.bequeath_multiple import bequeath_multiple
from abjad.helpers.container_contents_scale import container_contents_scale
from abjad.helpers.get_parent_and_index import get_parent_and_index
from abjad.helpers.iterate import iterate
from abjad.helpers.leaf_duration_change import leaf_duration_change
from abjad.helpers.remove_powers_of_two import _remove_powers_of_two
from abjad.rational.rational import Rational


def measures_subsume(expr):
   r'''Subsume all measures in expr containing only top-level tuplet.
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

   from abjad.measure.base import _Measure
   from abjad.tuplet.tuplet import _Tuplet
   for measure in iterate(expr, _Measure): 
      if len(measure) == 1:
         if isinstance(measure[0], _Tuplet):
            tuplet = measure[0]
            tuplet_multiplier = tuplet.duration.multiplier
            tuplet_denominator = tuplet_multiplier._d
            reduced_denominator = _remove_powers_of_two(tuplet_denominator)
            meter = measure.meter.effective
            meter_rational = Rational(meter.numerator, meter.denominator)
            numerator = meter_rational._n * reduced_denominator
            denominator = meter_rational._d * reduced_denominator
            measure.meter = (numerator, denominator)
            meter_multiplier = measure.meter.effective.multiplier
            written_adjustment = tuplet_multiplier / meter_multiplier
            #bequeath_multiple([tuplet], tuplet[:])
            parent, index = get_parent_and_index([tuplet])
            parent[index:index+1] = tuplet[:]
            container_contents_scale(measure, written_adjustment)
