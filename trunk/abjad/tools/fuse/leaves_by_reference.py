from abjad.tools import check
from abjad.tools import componenttools
from abjad.tools import leaftools


def leaves_by_reference(leaves):
   '''Fuse duration of all leaves in leaves.
      Rewrite duration of first leaf in leaf equal to sum.
      Detach all leaves other than first from score.
      Return list holding first leaf only.'''

   check.assert_components(leaves, contiguity = 'thread')
   if len(leaves) <= 1:
      return leaves
   total_written = sum([leaf.duration.written for leaf in leaves])
   componenttools.detach(leaves[1:])
   #return leaftools.scale_binary(leaves[0], total_written)
   return leaftools.duration_change(leaves[0], total_written)
