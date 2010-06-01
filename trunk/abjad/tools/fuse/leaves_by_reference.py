from abjad.tools import check
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import leaftools


def leaves_by_reference(leaves):
   r'''Fuse thread-contiguous `leaves`::

      abjad> staff = Staff(construct.scale(4))
      abjad> fuse.leaves_by_reference(staff[1:])
      [Note(d', 4.)]
      abjad> f(staff)
      \new Staff {
         c'8
         d'4.
      }
   
   Rewrite duration of first leaf in `leaves`.

   Detach all leaves in `leaves` other than first leaf from score.

   Return list of first leaf in `leaves`.
   '''

   check.assert_components(leaves, contiguity = 'thread')
   if len(leaves) <= 1:
      return leaves
   total_preprolated = durtools.sum_preprolated(leaves)
   componenttools.detach(leaves[1:])
   return leaftools.duration_preprolated_change(leaves[0], total_preprolated)
