from abjad.helpers.iterate import iterate
from abjad.helpers.measure_scale_and_remeter import measure_scale_and_remeter
from abjad.helpers.measures_spin import measures_spin
from abjad.rational.rational import Rational


def measures_concentrate(expr, concentration_pair):
   '''Iterate expr. For every measure in expr,
      spin measure by the first element in concentration_pair and
      scale measure by the inverse of the second element in concentration_pair.
   '''

   assert isinstance(concentration_pair, tuple)
   assert len(concentration_pair) == 2
   spin_count, scalar_denominator = concentration_pair

   for measure in iterate(expr, '_Measure'):
      measures_spin(measure, spin_count)
      multiplier = Rational(1, scalar_denominator)
      measure_scale_and_remeter(measure, multiplier)
