from abjad.exceptions import MissingSpannerError
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_leaves_in_tie_chain(tie_chain):
   '''Return Python list of leaves in tie chain.'''

   assert is_tie_chain(tie_chain)

   try:
      return tie_chain[0].tie.spanner.leaves
   except MissingSpannerError:
      assert len(tie_chain) == 1
      leaves = (tie_chain[0], )
      return leaves
