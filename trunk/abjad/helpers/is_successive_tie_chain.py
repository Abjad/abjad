from abjad.helpers.contiguity import _are_successive_components
from abjad.helpers.is_tie_chain import _is_tie_chain


def _is_successive_tie_chain(expr):
   '''True when expr is a tie chain with all leaves successive.'''

   return _is_tie_chain(expr) and _are_successive_components(list(expr))
