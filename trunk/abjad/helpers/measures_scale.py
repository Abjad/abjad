from abjad.helpers.iterate import iterate
from abjad.helpers.container_contents_scale import container_contents_scale
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.helpers.make_best_meter import _make_best_meter
from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
from abjad.measure.measure import _Measure
from abjad.meter.meter import Meter
from abjad.rational.rational import Rational


def measures_scale(expr, multiplier = Rational(1)):
   '''Iterate expr. For every measure in expr:

         1. multiply measure's meter by multiplier
         2. scale measure's contents to fit new meter

      Extends container_contents_scale( ).
      Returns None because iterates possibly many measures.

      This might best be a bound method on RigidMeasure.'''

   for measure in iterate(expr, _Measure):

      if multiplier == Rational(1):
         continue

      if _is_power_of_two(multiplier) and 1 <= multiplier:
         old_numerator = measure.meter.effective.duration._n
         old_denominator = measure.meter.effective.duration._d
         new_denominator = old_denominator / multiplier._n
         new_meter = Meter(old_numerator, new_denominator)
      else:
         old_meter = measure.meter.effective
         old_denominator = old_meter.denominator
         old_duration = old_meter.duration
         new_duration = multiplier * old_duration
         new_meter = _make_best_meter(
            new_duration, [old_denominator], multiplier._d)
      measure.meter = new_meter

      contents_multiplier_denominator = _next_least_power_of_two(multiplier._d)
      contents_multiplier = Rational(
         multiplier._n, contents_multiplier_denominator)
      container_contents_scale(measure, contents_multiplier)
