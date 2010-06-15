from abjad.tools import componenttools
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
   from abjad.tools import componenttools

   assert componenttools.all_are_thread_contiguous_components(leaves)

   if len(leaves) <= 1:
      return leaves

   total_preprolated = componenttools.sum_preprolated_duration_of_components(leaves)
   componenttools.remove_component_subtree_from_score_and_spanners(leaves[1:])
   return leaftools.change_leaf_preprolated_duration(
      leaves[0], total_preprolated)
