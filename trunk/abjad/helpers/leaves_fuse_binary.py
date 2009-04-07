from abjad.helpers.assert_components import assert_components
from abjad.helpers.leaf_scale_binary import leaf_scale_binary


def leaves_fuse_binary(leaves):
   '''Fuse duration of all leaves in leaves.
      Rewrite duration of first leaf in leaf equal to sum.
      Detach all leaves other than first from score.
      Return list holding first leaf only.'''

   assert_components(leaves, contiguity = 'thread')
   if len(leaves) <= 1:
      return leaves
   total_written = sum([leaf.duration.written for leaf in leaves])
   for leaf in leaves[1:]:
      leaf.detach( )
   return leaf_scale_binary(leaves[0], total_written)
