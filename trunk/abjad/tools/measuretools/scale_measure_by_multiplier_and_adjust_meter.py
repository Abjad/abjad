from abjad.tools.metertools import Meter
from abjad.core import Rational
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import mathtools


def scale_measure_by_multiplier_and_adjust_meter(measure, multiplier = Rational(1)):
   r'''Multiply the duration of every element in measure by multiplier.
      Then rewrite the meter of measure as appropriate.

      Return treated measure.

      Like magic.

      Example::

         abjad> t = RigidMeasure((3, 8), macros.scale(3))
         abjad> measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Rational(2, 3))
         abjad> print t.format

              \time 3/12
              \scaleDurations #'(2 . 3) {
                      c'8
                      d'8
                      e'8
              }

   .. versionchanged:: 1.1.2
      renamed ``measuretools.scale_and_remeter( )`` to
      ``measuretools.scale_measure_by_multiplier_and_adjust_meter( )``.
   '''

   from abjad.tools import containertools

   if multiplier == 0:
      raise ZeroDivisionError

   old_meter = measure.meter.effective
   old_pair = (old_meter.numerator, old_meter.denominator)
   old_multiplier = old_meter.multiplier
   old_multiplier_pair = (old_multiplier.numerator, old_multiplier.denominator)

   multiplied_pair = durtools.multiply_duration_pair(old_multiplier_pair, multiplier)
   reduced_pair = durtools.multiply_duration_pair_and_reduce_factors(
      old_multiplier_pair, multiplier)

   if reduced_pair != multiplied_pair:
      new_pair = durtools.multiply_duration_pair_and_try_to_preserve_numerator(
         old_pair, multiplier)      
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
      remaining_multiplier = Rational(*reduced_pair)
      if remaining_multiplier != Rational(1):
         containertools.scale_contents_of_container(measure, remaining_multiplier)
   elif componenttools.all_are_components_scalable_by_multiplier(measure[:], multiplier):
      containertools.scale_contents_of_container(measure, multiplier)
      if old_meter.nonbinary or not mathtools.is_power_of_two(multiplier):
         new_pair = durtools.multiply_duration_pair_and_reduce_factors(old_pair, multiplier)
      ## multiplier is a negative power of two, like 1/2, 1/4, etc.
      elif multiplier < Rational(0):
         new_pair = durtools.multiply_duration_pair(old_pair, multiplier)
      ## multiplier is a nonnegative power of two, like 0, 1, 2, 4, etc.
      elif Rational(0) < multiplier:
         new_pair = durtools.multiply_duration_pair_and_try_to_preserve_numerator(
            old_pair, multiplier)
      elif multiplier == Rational(0):
         raise ZeroDivisionError
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
   else:
      new_pair = durtools.multiply_duration_pair_and_try_to_preserve_numerator(
         old_pair, multiplier)
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
      remaining_multiplier = multiplier / new_meter.multiplier
      if remaining_multiplier != Rational(1):
         containertools.scale_contents_of_container(measure, remaining_multiplier)
   return measure
