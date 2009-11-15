from abjad.measure import _Measure
from abjad.tools.iterate.naive_backward import naive_backward as \
   iterate_naive_backwards


def measures_backward_in(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Yield right-to-left measures in `expr`. ::

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

      abjad> for measure in iterate.measures_backward_in(staff):
      ...     measure
      ... 
      RigidMeasure(2/8, [g'8, a'8])
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [c'8, d'8])

   Use the optional `start` and `stop` keyword parameters
   to control indices of iteration. ::

      abjad> for measure in iterate.measures_backward_in(staff, start = 1):
      ...     measure
      ... 
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [c'8, d'8])

   ::

      abjad> for measure in iterate.measures_backward_in(staff, start = 0, stop = 2):
      ...     measure
      ... 
      RigidMeasure(2/8, [g'8, a'8])
      RigidMeasure(2/8, [e'8, f'8])

   .. note:: naive iteration ignores threads.
   '''

   return iterate_naive_backwards(expr, _Measure, start = start, stop = stop)
