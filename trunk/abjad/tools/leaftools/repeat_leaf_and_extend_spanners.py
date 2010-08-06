from abjad.components._Leaf import _Leaf
from abjad.tools import componenttools
from abjad.tools import iterate


def repeat_leaf_and_extend_spanners(leaf, total = 1):
   r'''.. versionadded:: 1.1.1

   Clone and splice `leaf` `total` times::

      abjad> staff = Staff(macros.scale(4))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> leaftools.repeat_leaf_and_extend_spanners(staff[0], total = 3)
      
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

   .. versionchanged:: 1.1.2
      renamed ``leaftools.clone_and_splice_leaf( )`` to
      ``leaftools.repeat_leaf_and_extend_spanners( )``.
   '''

   leaf.splice(componenttools.clone_components_and_remove_all_spanners([leaf], total - 1))
