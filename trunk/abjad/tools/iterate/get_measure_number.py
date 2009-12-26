from abjad.tools.iterate.get_nth_measure import get_nth_measure


def get_measure_number(expr, measure_number):
   r'''.. versionadded:: 1.1.2

   Return `measure_number` in `expr`. ::

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
      abjad> iterate.get_measure_number(t, 3)
      RigidMeasure(2/8, [g'8, a'8])

   .. note:: measures number from 1.
   '''

   if measure_number < 1:
      raise ValueError('measure numbers allow only positive integers.')

   ## calculate measure index
   measure_index = measure_number - 1

   ## return measure
   return get_nth_measure(expr, measure_index)
