from abjad.tools import iterate
from abjad.tools.leaftools.divide_leaf_meiotically import \
   divide_leaf_meiotically


def divide_leaves_in_expr_meiotically(expr, n = 2):
   r'''.. versionadded:: 1.1.1

   Divide leaves meiotically in `expr` `n` times::

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
      
      abjad> leaftools.divide_leaves_in_expr_meiotically(staff[2:], n = 4)
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'32
         e'32
         e'32
         e'32
         f'32
         f'32
         f'32
         f'32 ]
      }

   Replace every leaf in `expr` with `n` new leaves.

   Preserve parentage and spanners.

   Allow divisions into only ``1, 2, 4, 8, 16, ...`` and other
   nonnegative integer powers of ``2``.

   Produce only leaves and never tuplets or other containers.

   Return none.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.meiose( )`` to 
      ``leaftools.divide_leaves_in_expr_meiotically( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.divide_leaves_meiotically_in( )`` to
      ``leaftools.divide_leaves_in_expr_meiotically( )``.
   '''

   ## can not wrap with update control because of leaf.splice( ) ##
   #expr.parentage.root._update._forbidUpdate( )
   for leaf in iterate.leaves_backward_in_expr(expr):
      divide_leaf_meiotically(leaf, n)
   #expr.parentage.root._update._allowUpdate( )
   #expr.parentage.root._update._updateAll( )
