from abjad.rational import Rational
from abjad.tools import iterate
from abjad.tools.measuretools.scale_and_remeter import scale_and_remeter
from abjad.tools.measuretools.spin import spin


def concentrate(expr, concentration_pairs, cyclic = True):
   '''Expr may be any Abjad expression.
   Concentration_pairs a Python list of pairs,
   each of the form (spin_count, scalar_denominator).
   Both spin_count and scalar_denominator must be positive integers.

   Iterate expr. For every measure in expr, 
   spin measure by the spin_count element in concentration_pair and
   scale measure by 1/scalar_denominator element in concentration_pair.

   Return Python list of transformed measures.

   Example::

      abjad> t = RigidMeasure((3, 16), construct.run(3, Rational(1, 16)))
      abjad> print(measuretools.concentrate(t, [(3, 3)])[0])
      |9/48, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32|

   Example::

      abjad> t = RigidMeasure((3, 16), construct.run(3, Rational(1, 16)))
      abjad> print(measuretools.concentrate(t, [(3, 2)])[0])
      |9/32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32|
   
   Example::

      abjad> t = RigidMeasure((3, 16), construct.run(3, Rational(1, 16)))
      abjad> print(measuretools.concentrate(t, [(3, 1)])[0])
      |9/16, c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16|
   '''

   assert isinstance(concentration_pairs, list)
   assert all([isinstance(pair, tuple) for pair in concentration_pairs])

   result = [ ]
   num_pairs = len(concentration_pairs)
   for i, measure in enumerate(iterate.measures_forward_in(expr)):
      concentration_pair = concentration_pairs[i % num_pairs]
      assert isinstance(concentration_pair, tuple)
      spin_count, scalar_denominator = concentration_pair
      spin(measure, spin_count)
      multiplier = Rational(1, scalar_denominator)
      scale_and_remeter(measure, multiplier)
      result.append(measure)

   return result
