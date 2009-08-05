from abjad.measure.measure import _Measure
from abjad.meter import Meter
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import iterate


def spin(expr, n):
   r'''Iterate expr. For each measure in expr,
      multiply contents of measure by n.

      Extends containertools.contents_multiply( ) with meter-handling.

      Example:

      t = RigidMeasure((3, 8), construct.scale(3))
      measuretools.spin(t, 3)

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

   from abjad.tools import containertools
   assert isinstance(n, int)
   assert n > 0

   for measure in iterate.naive(expr, _Measure):
      old_meter = measure.meter.effective
      containertools.contents_multiply(measure, n)
      old_pair = (old_meter.numerator, old_meter.denominator)
      new_pair = durtools.pair_multiply_naive(old_pair, Rational(n))
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
