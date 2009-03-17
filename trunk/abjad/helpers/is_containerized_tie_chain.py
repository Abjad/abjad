from abjad.helpers.are_containerized_components import _are_containerized_components
from abjad.helpers.is_tie_chain import _is_tie_chain


def _is_containerized_tie_chain(expr):
   '''True when expr is a tie chain with all containerized leaves.
      IE, True when tie chain crosses no container boundaries.'''

   return _is_tie_chain(expr) and _are_containerized_components(list(expr))
