from abjad.tools import iterate
from abjad.tools.leaftools.color_leaf import color_leaf


def color_leaves_in(expr, color):
   r""".. versionadded:: 1.1.2

   Color leaves in `expr` with `color`::

      abjad> staff = Staff([Note(1, (3, 16)), Rest((3, 16)), Skip((3, 16)), Chord([0, 1, 9], (3, 16))])
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         cs'8. [
         r8.
         s8.
         <c' cs' a'>8. ]
      }
      
   ::
      
      abjad> leaftools.color_leaves_in(staff, 'red')
      
   ::
      
      abjad> f(staff)
      \new Staff {
         \once \override Accidental #'color = #red
         \once \override Dots #'color = #red
         \once \override NoteHead #'color = #red
         cs'8. [
         \once \override Dots #'color = #red
         \once \override Rest #'color = #red
         r8.
         s8.
         \once \override Accidental #'color = #red
         \once \override Dots #'color = #red
         \once \override NoteHead #'color = #red
         <c' cs' a'>8. ]
      }

   Return none.
   """

   for leaf in iterate.leaves_forward_in_expr(expr):
      color_leaf(leaf, color)
