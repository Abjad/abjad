from abjad.leaf import _Leaf
from abjad.tools.iterate.naive_forward_in import naive_forward_in as \
   iterate_naive_forward_in


def leaves_forward_in(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Yield left-to-right leaves in `expr`. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
              {
                      \time 2/8
                      c'8
                      d'8
              }
              {
                      \time 2/8
                      e'8
                      f'8
              }
              {
                      \time 2/8
                      g'8
                      a'8
              }
      }

   ::

      abjad> for leaf in iterate.leaves_forward_in(staff):
      ...     leaf
      ... 
      Note(c', 8)
      Note(d', 8)
      Note(e', 8)
      Note(f', 8)
      Note(g', 8)
      Note(a', 8)

   Use the optional `start` and `stop` keyword parameters to control
   the start and stop indices of iteration. ::

      abjad> for leaf in iterate.leaves_forward_in(staff, start = 3):
      ...     leaf
      ... 
      Note(f', 8)
      Note(g', 8)
      Note(a', 8)

   ::

      abjad> for leaf in iterate.leaves_forward_in(staff, start = 0, stop = 3):
      ...     leaf
      ... 
      Note(c', 8)
      Note(d', 8)
      Note(e', 8)

   ::

      abjad> for leaf in iterate.leaves_forward_in(staff, start = 2, stop = 4):
      ...     leaf
      ... 
      Note(e', 8)
      Note(f', 8)

   .. note:: naive iteration ignores threads.
   '''

   return iterate_naive_forward_in(expr, _Leaf, start = start, stop = stop)
