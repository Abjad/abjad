from abjad.tools.iterate.get_nth_measure_in_expr import get_nth_measure_in_expr


def get_measure_number_in_expr(expr, measure_number):
   r'''.. versionadded:: 1.1.2

   Return `measure_number` in `expr`. ::

      abjad> t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
      abjad> pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
      abjad> f(t)
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
      abjad> iterate.get_measure_number_in_expr(t, 3)
      RigidMeasure(2/8, [g'8, a'8])

   .. note:: measures number from 1.

   .. versionchanged:: 1.1.2
      renamed ``iterate.get_measure_number( )`` to
      ``iterate.get_measure_number_in_expr( )``.
   '''

   if measure_number < 1:
      raise ValueError('measure numbers allow only positive integers.')

   ## calculate measure index
   measure_index = measure_number - 1

   ## return measure
   return get_nth_measure_in_expr(expr, measure_index)
