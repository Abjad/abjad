from abjad.measure import _Measure
from abjad.tools.iterate.get_nth_component import get_nth_component as \
   iterate_get_nth_component


def get_nth_measure(expr, n = 0):
   r'''.. versionadded:: 1.1.2

   Return measure `n` in `expr`. ::

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

   Read forward for positive values of `n`. ::

      abjad> for n in range(3):
      ...     iterate.get_nth_measure(staff, n)
      ... 
      RigidMeasure(2/8, [c'8, d'8])
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [g'8, a'8])

   Read backward for negative values of `n`. ::

      abjad> for n in range(3, -1, -1):
      ...     iterate.get_nth_measure(staff, n)
      ... 
      RigidMeasure(2/8, [g'8, a'8])
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [c'8, d'8])
         
   .. todo:: implement ``iterate.measures_forward_in(expr, i = 0, j = None)``
      as a companion to this function.
   '''

   return iterate_get_nth_component(expr, _Measure, n)
