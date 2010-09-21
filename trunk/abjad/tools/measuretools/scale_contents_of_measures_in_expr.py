from abjad.tools.metertools import Meter
from abjad.core import Rational
from abjad.tools import mathtools
from abjad.tools import marktools
from abjad.tools import metertools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr


def scale_contents_of_measures_in_expr(expr, multiplier = Rational(1)):
   '''Iterate expr. For every measure in expr:

      1. multiply measure's meter by multiplier
      2. scale measure's contents to fit new meter

   Extends containertools.scale_contents_of_container( ).
   Returns None because iterates possibly many measures.

   This might best be a bound method on Measure.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.scale( )`` to
      ``measuretools.scale_contents_of_measures_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.scale_measure_contents_in( )`` to
      ``measuretools.scale_contents_of_measures_in_expr( )``.
   '''

   from abjad.tools import containertools
   
   for measure in iterate_measures_forward_in_expr(expr):

      if multiplier == Rational(1):
         continue

      if mathtools.is_power_of_two(multiplier) and 1 <= multiplier:
         old_numerator = marktools.get_effective_time_signature(measure).numerator
         old_denominator = marktools.get_effective_time_signature(measure).denominator
         new_denominator = old_denominator / multiplier.numerator
         new_meter = metertools.Meter(old_numerator, new_denominator)
      else:
         old_meter = marktools.get_effective_time_signature(measure)
         old_denominator = old_meter.denominator
         old_duration = old_meter.duration
         new_duration = multiplier * old_duration
         new_meter = metertools.duration_and_possible_denominators_to_meter(
            new_duration, [old_denominator], multiplier.denominator)
      measure._attach_explicit_meter(new_meter.numerator, new_meter.denominator)

      contents_multiplier_denominator = \
         mathtools.greatest_power_of_two_less_equal(multiplier.denominator)
      contents_multiplier = Rational(
         multiplier.numerator, contents_multiplier_denominator)
      containertools.scale_contents_of_container(measure, contents_multiplier)
