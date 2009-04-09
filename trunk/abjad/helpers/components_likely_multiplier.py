from abjad.helpers.assert_components import assert_components
from abjad.tools import tietools
from abjad.tools import iterate
from abjad.tools import mathtools
from abjad.tools import listtools
from abjad.tools import tietools
from abjad.rational.rational import Rational


def _components_likely_multiplier(components):
   '''Heuristic function to guess at a likely multiplier
      that may have been applied to the components in list
      at some point during a previous composition-time transform.

      Otherwise, return None.

      Implemented to help reverse measure subsumption.'''

   assert_components(components)

   chain_duration_numerators = [ ]
   for expr in iterate.chained_contents(components):
      if tietools.is_chain(expr):
         chain_duration = tietools.duration_written(expr)   
         chain_duration_numerators.append(chain_duration._n)
       
   if len(listtools.unique(chain_duration_numerators)) == 1:
      numerator = chain_duration_numerators[0]
      denominator = mathtools.next_least_power_of_two(numerator)
      likely_multiplier = Rational(numerator, denominator)
      return likely_multiplier
