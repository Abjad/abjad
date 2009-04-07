from abjad.helpers.contents_multiply import contents_multiply
from abjad.helpers.iterate import iterate
from abjad.helpers.pair_multiply_naive import _pair_multiply_naive
from abjad.meter.meter import Meter
from abjad.rational.rational import Rational


def measures_spin(expr, n):
   r'''Iterate expr. For each measure in expr,
      multiply contents of measure by n.

      Extends contents_multiply( ) with meter-handling.

      Example:

      t = RigidMeasure((3, 8), scale(3))
      measures_spin(t, 3)

           \time 9/8
           c'8
           d'8
           e'8
           c'8
           d'8
           e'8
           c'8
           d'8
           e'8'''

   assert isinstance(n, int)
   assert n > 0

   from abjad.measure.measure import _Measure
   for measure in iterate(expr, _Measure):
      old_meter = measure.meter.effective
      contents_multiply(measure, n)
      old_pair = (old_meter.numerator, old_meter.denominator)
      new_pair = _pair_multiply_naive(old_pair, Rational(n))
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
