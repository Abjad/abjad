from abjad.exceptions.exceptions import MissingSpannerError
from abjad.helpers.is_tie_chain import _is_tie_chain


def tie_chain_get_leaves(tie_chain):
   '''Return Python list of leaves in tie chain.'''

   assert _is_tie_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.leaves
   except MissingSpannerError:
      assert len(tie_chain) == 1
      return [tie_chain[0]]
