from abjad.helpers.are_scalable_components import _are_scalable_components
from abjad.helpers.container_contents_scale import container_contents_scale
from abjad.helpers.pair_multiply_naive import _pair_multiply_naive
from abjad.helpers.pair_multiply_constant_numerator import _pair_multiply_constant_numerator
from abjad.helpers.pair_multiply_reduce_factors import _pair_multiply_reduce_factors
from abjad.meter.meter import Meter
from abjad.rational.rational import Rational


def measure_scale_and_remeter(measure, multiplier = Rational(1)):
   r'''Multiply the duration of every element in measure by multiplier.
      Then rewrite the meter of measure as appropriate.

      Like magic.

      Example:

      t = RigidMeasure((3, 8), scale(3))
      measure_scale_and_remeter(t, Rational(2, 3))

           \time 3/12
           \scaleDurations #'(2 . 3) {
                   c'8
                   d'8
                   e'8
           }'''

   old_meter = measure.meter.effective
   old_pair = (old_meter.numerator, old_meter.denominator)
   old_multiplier = old_meter.multiplier
   old_multiplier_pair = (old_multiplier._n, old_multiplier._d)

   multiplied_pair = _pair_multiply_naive(old_multiplier_pair, multiplier)
   reduced_pair = _pair_multiply_reduce_factors(old_multiplier_pair, multiplier)

   if reduced_pair != multiplied_pair:
      new_pair = _pair_multiply_constant_numerator(old_pair, multiplier)      
      new_meter = Meter(new_pair)
      measure.meter = new_meter
      remaining_multiplier = Rational(*reduced_pair)
      if remaining_multiplier != Rational(1):
         container_contents_scale(measure, remaining_multiplier)
   elif _are_scalable_components(measure[:], multiplier):
      container_contents_scale(measure, multiplier)
      new_pair = _pair_multiply_reduce_factors(old_pair, multiplier)
      new_meter = Meter(new_pair)
      measure.meter = new_meter
   else:
      new_pair = _pair_multiply_constant_numerator(old_pair, multiplier)
      new_meter = Meter(new_pair)
      measure.meter = new_meter
      remaining_multiplier = multiplier / new_meter.multiplier
      if remaining_multiplier != Rational(1):
         container_contents_scale(measure, remaining_multiplier)
