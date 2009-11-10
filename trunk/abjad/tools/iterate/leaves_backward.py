from abjad.leaf import _Leaf
from abjad.tools.iterate.naive_backward import naive_backward as \
   iterate_naive_backwards


def leaves_backward(expr):
   r'''.. versionadded:: 1.1.2

   Yield right-to-left leaves in `expr`. ::

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

      abjad> for leaf in iterate.leaves_backward(t):
      ...     leaf
      ... 
      Note(a', 8)
      Note(g', 8)
      Note(f', 8)
      Note(e', 8)
      Note(d', 8)
      Note(c', 8)

   .. note:: this naive iteration ignores threads.

   .. todo:: generalize with optional start and stop values.
   '''

   return iterate_naive_backwards(expr, _Leaf)
