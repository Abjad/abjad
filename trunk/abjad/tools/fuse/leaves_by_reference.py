from abjad.tools import check
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import leaftools


def leaves_by_reference(leaves):
   '''Fuse duration of all leaves in leaves.
      Rewrite duration of first leaf in leaf equal to sum.
      Detach all leaves other than first from score.
      Return list holding first leaf only.'''

   check.assert_components(leaves, contiguity = 'thread')
   if len(leaves) <= 1:
      return leaves
   total_preprolated = durtools.sum_preprolated(leaves)
   componenttools.detach(leaves[1:])
   ## TODO: Rename leaftools.duration_change to leaftools.duration_preprolated_change ##
   return leaftools.duration_change(leaves[0], total_preprolated)
