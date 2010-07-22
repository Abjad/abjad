from abjad.measure import _Measure
from abjad.tools.iterate.get_nth_component_in_expr import get_nth_component_in_expr


def get_nth_measure_in_expr(expr, n = 0):
   r'''.. versionadded:: 1.1.2

   Return measure `n` in `expr`. ::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
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
      ...     iterate.get_nth_measure_in_expr(staff, n)
      ... 
      RigidMeasure(2/8, [c'8, d'8])
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [g'8, a'8])

   Read backward for negative values of `n`. ::

      abjad> for n in range(3, -1, -1):
      ...     iterate.get_nth_measure_in_expr(staff, n)
      ... 
      RigidMeasure(2/8, [g'8, a'8])
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [c'8, d'8])
         
   .. todo:: implement ``iterate.measures_forward_in_expr(expr, i = 0, j = None)``
      as a companion to this function.

   .. versionchanged:: 1.1.2
      renamed ``iterate.get_nth_measure( )`` to
      ``iterate.get_nth_measure_in_expr( )``.
   '''

   return get_nth_component_in_expr(expr, _Measure, n)
