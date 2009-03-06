from abjad.helpers.are_components import _are_components
from abjad.helpers.is_tie_chain import _is_tie_chain
from abjad.helpers.iterate_chained_contents import iterate_chained_contents
from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
from abjad.helpers.tie_chain_written import tie_chain_written
from abjad.helpers.unique import unique
from abjad.rational.rational import Rational


def _components_likely_multiplier(components):
   '''Heuristic function to guess at a likely multiplier
      that may have been applied to the components in list
      at some point during a previous composition-time transform.

      Otherwise, return None.

      Implemented to help reverse measure subsumption.'''

   assert _are_components(components)

   chain_duration_numerators = [ ]
   for expr in iterate_chained_contents(components):
      if _is_tie_chain(expr):
         chain_duration = tie_chain_written(expr)   
         chain_duration_numerators.append(chain_duration._n)
       
   if len(unique(chain_duration_numerators)) == 1:
      numerator = chain_duration_numerators[0]
      denominator = _next_least_power_of_two(numerator)
      likely_multiplier = Rational(numerator, denominator)
      return likely_multiplier
