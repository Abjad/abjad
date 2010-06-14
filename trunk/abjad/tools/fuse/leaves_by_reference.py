from abjad.tools import check
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import leaftools


def leaves_by_reference(leaves):
   r'''Fuse thread-contiguous `leaves`::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
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
   componenttools.remove_component_subtree_from_score_and_spanners(leaves[1:])
   return leaftools.change_leaf_preprolated_duration(
      leaves[0], total_preprolated)
