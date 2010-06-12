from abjad.tools import componenttools
from abjad.tools.tietools.is_chain import is_chain


def truncate(tie_chain):
   '''Detach all leaves of tie chain after the first.
      Unspan and return length-1 tie chain.
   '''
   
   assert is_chain(tie_chain)

   for leaf in tie_chain[1:]:
      componenttools.remove_component_subtree_from_score_and_spanners([leaf])

   first = tie_chain[0]

   first.tie.unspan( )
   
   return first.tie.chain
