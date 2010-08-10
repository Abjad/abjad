from abjad.components._Measure import _Measure
from abjad.tools.componenttools.iterate_components_backward_in_expr import iterate_components_backward_in_expr


def iterate_measures_backward_in_expr(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Yield right-to-left measures in `expr`. ::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
      abjad> pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
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

      abjad> for measure in measuretools.iterate_measures_backward_in_expr(staff):
      ...     measure
      ... 
      RigidMeasure(2/8, [g'8, a'8])
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [c'8, d'8])

   Use the optional `start` and `stop` keyword parameters
   to control indices of iteration. ::

      abjad> for measure in measuretools.iterate_measures_backward_in_expr(staff, start = 1):
      ...     measure
      ... 
      RigidMeasure(2/8, [e'8, f'8])
      RigidMeasure(2/8, [c'8, d'8])

   ::

      abjad> for measure in measuretools.iterate_measures_backward_in_expr(staff, start = 0, stop = 2):
      ...     measure
      ... 
      RigidMeasure(2/8, [g'8, a'8])
      RigidMeasure(2/8, [e'8, f'8])

   .. note:: naive iteration ignores threads.

   .. versionchanged:: 1.1.2
      renamed ``iterate.measures_backward_in( )`` to
      ``measuretools.iterate_measures_backward_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.measures_backward_in_expr( )`` to
      ``measuretools.iterate_measures_backward_in_expr( )``.
   '''

   return iterate_components_backward_in_expr(expr, _Measure, start = start, stop = stop)
