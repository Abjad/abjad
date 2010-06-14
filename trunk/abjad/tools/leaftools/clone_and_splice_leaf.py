from abjad.leaf import _Leaf
from abjad.tools import componenttools
from abjad.tools import iterate


def clone_and_splice_leaf(leaf, total = 1):
   r'''.. versionadded:: 1.1.1

   Clone and splice `leaf` `total` times::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> leaftools.clone_and_splice_leaf(staff[0], total = 3)
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 [
         c'8
         c'8
         d'8
         e'8
         f'8 ]
      }

   Preserve `leaf` written duration.

   Preserve parentage and spanners.

   Return none.
   '''

   leaf.splice(componenttools.clone_components_and_remove_all_spanners([leaf], total - 1))
