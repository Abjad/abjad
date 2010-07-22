from abjad.tools.iterate.get_measure_number_in_expr import get_measure_number_in_expr
from abjad.tools.iterate.get_nth_leaf_in_expr import get_nth_leaf_in_expr


def get_leaf_at_index_from_measure_number_in_expr(expr, measure_number, leaf_index):
   r'''.. versionadded:: 1.1.2

   Return `leaf_index` at `measure_number` in `expr`. ::

      abjad> t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
      abjad> pitchtools.diatonicize(t)
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

   ::

      abjad> iterate.get_leaf_at_index_from_measure_number_in_expr(t, 2, 0)
      Note(e', 8)

   .. versionchanged:: 1.1.2
      renamed ``iterate.get_measure_leaf( )`` to
      ``iterate.get_leaf_at_index_from_measure_number_in_expr( )``.
   '''

   ## return leaf in measure
   return get_nth_leaf_in_expr(get_measure_number_in_expr(expr, measure_number), leaf_index)
