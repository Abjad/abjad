from abjad.components.Skip import Skip
from abjad.tools import iterate


def replace_leaves_with_skips_in(expr):
   r'''.. versionadded:: 1.1.1

   Replace leaves with skips in `expr`::

      abjad> staff = Staff(RigidMeasure((2, 8), macros.scale(2)) * 2)
      abjad> leaftools.replace_leaves_with_skips_in(staff[0])
      abjad> print staff.format
      \new Staff {
            \time 2/8
            s8
            s8
            \time 2/8
            c'8
            d'8
      }

   Return none.
   '''

   for leaf in iterate.leaves_forward_in_expr(expr):
      Skip(leaf)
