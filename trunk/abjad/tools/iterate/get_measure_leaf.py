from abjad.tools.iterate.get_nth_leaf import get_nth_leaf
from abjad.tools.iterate.get_nth_measure import get_nth_measure


def get_measure_leaf(expr, measure_number, leaf_index):
   r'''.. versionadded:: 1.1.2

   Return `leaf_index` at `measure_number` in `expr`. ::

      abjad> t = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
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

      abjad> iterate.get_measure_leaf(t, 2, 0)
      Note(e', 8)
   '''

   ## calculate measure index from measure number
   measure_index = measure_number - 1

   ## return leaf in measure
   return get_nth_leaf(get_nth_measure(expr, measure_index), leaf_index)
