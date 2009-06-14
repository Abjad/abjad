from abjad.meter import Meter
from abjad.rational import Rational
from abjad.tools import check
from abjad.tools import durtools
from abjad.tools import mathtools


def scale_and_remeter(measure, multiplier = Rational(1)):
   r'''Multiply the duration of every element in measure by multiplier.
      Then rewrite the meter of measure as appropriate.

      Return treated measure.

      Like magic.

      Example::

         abjad> t = RigidMeasure((3, 8), construct.scale(3))
         abjad> measuretools.scale_and_remeter(t, Rational(2, 3))
         abjad> print t.format

              \time 3/12
              \scaleDurations #'(2 . 3) {
                      c'8
                      d'8
                      e'8
              }'''

   from abjad.tools import containertools

   if multiplier == 0:
      raise ZeroDivisionError

   old_meter = measure.meter.effective
   old_pair = (old_meter.numerator, old_meter.denominator)
   old_multiplier = old_meter.multiplier
   old_multiplier_pair = (old_multiplier._n, old_multiplier._d)

   multiplied_pair = durtools.pair_multiply_naive(
      old_multiplier_pair, multiplier)
   reduced_pair = durtools.pair_multiply_reduce_factors(
      old_multiplier_pair, multiplier)

   if reduced_pair != multiplied_pair:
      new_pair = durtools.pair_multiply_constant_numerator(
         old_pair, multiplier)      
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
      remaining_multiplier = Rational(*reduced_pair)
      if remaining_multiplier != Rational(1):
         containertools.contents_scale(measure, remaining_multiplier)
   elif check.are_scalable(measure[:], multiplier):
      containertools.contents_scale(measure, multiplier)
      if old_meter.nonbinary or not mathtools.is_power_of_two(multiplier):
         new_pair = durtools.pair_multiply_reduce_factors(
            old_pair, multiplier)
      ## multiplier is a negative power of two, like 1/2, 1/4, etc.
      elif multiplier < Rational(0):
         new_pair = durtools.pair_multiply_naive(old_pair, multiplier)
      ## multiplier is a nonnegative power of two, like 0, 1, 2, 4, etc.
      elif multiplier > Rational(0):
         new_pair = durtools.pair_multiply_constant_numerator(
            old_pair, multiplier)
      elif multiplier == Rational(0):
         raise ZeroDivisionError
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
   else:
      new_pair = durtools.pair_multiply_constant_numerator(
         old_pair, multiplier)
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
      remaining_multiplier = multiplier / new_meter.multiplier
      if remaining_multiplier != Rational(1):
         containertools.contents_scale(measure, remaining_multiplier)
   return measure
