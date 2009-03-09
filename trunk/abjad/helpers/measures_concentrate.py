from abjad.helpers.iterate import iterate
from abjad.helpers.measure_scale_and_remeter import measure_scale_and_remeter
from abjad.helpers.measures_spin import measures_spin
from abjad.rational.rational import Rational


def measures_concentrate(expr, concentration_pair):
   '''Expr may be any Abjad expression.
      Concentration_pair of the form (spin_count, scalar_denominator).
      Both spin_count and scalar_denominator must be positive integers.

      Iterate expr. For every measure in expr, 
      spin measure by the spin_count element in concentration_pair and
      scale measure by 1/scalar_denominator element in concentration_pair.

      Return Python list of transformed measures.

      Examples:

      abjad> t = RigidMeasure((3, 16), run(3, Rational(1, 16)))
      abjad> print(measures_concentrate(t, (3, 3)[0])
      |9/48, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32|

      abjad> t = RigidMeasure((3, 16), run(3, Rational(1, 16)))
      abjad> print(measures_concentrate(t, (3, 2)[0])
      |9/32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32|
      
      abjad> t = RigidMeasure((3, 16), run(3, Rational(1, 16)))
      abjad> print(measures_concentrate(t, (3, 1)[0])
      |9/16, c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16|
   '''

   assert isinstance(concentration_pair, tuple)
   assert len(concentration_pair) == 2
   spin_count, scalar_denominator = concentration_pair

   result = [ ]
   for measure in iterate(expr, '_Measure'):
      measures_spin(measure, spin_count)
      multiplier = Rational(1, scalar_denominator)
      measure_scale_and_remeter(measure, multiplier)
      result.append(measure)

   return result
