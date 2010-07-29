from abjad.tools import iterate
from abjad.tools.leaftools.clone_and_splice_leaf import clone_and_splice_leaf


def clone_and_splice_leaves_in(expr, total = 1):
   r'''.. versionadded:: 1.1.1

   Clone and splice leaves in `expr` `total` times::

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
      
      abjad> result = leaftools.clone_and_splice_leaves_in(staff[2:], total = 3)
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         e'8
         e'8
         f'8
         f'8
         f'8 ]
      }

   Preserve leaf written durations.

   Preserve parentage and spanners.

   Return none.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.multiply( )`` to
      ``leaftools.clone_and_splice_leaves_in( )``.
   '''

   for leaf in iterate.leaves_backward_in_expr(expr):
      clone_and_splice_leaf(leaf, total)
