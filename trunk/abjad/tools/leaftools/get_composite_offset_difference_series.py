from abjad.tools import listtools
from abjad.tools.leaftools.get_composite_offset_series import \
   get_composite_offset_series


def get_composite_offset_difference_series(expr):
   r'''.. versionadded:: 1.1.2

   List time intervals between unique start and stop offsets 
   of `expr` leaves::

      abjad> staff_1 = Staff([FixedDurationTuplet((4, 8), construct.run(3))])
      abjad> staff_2 = Staff(construct.run(4))
      abjad> score = Score([staff_1, staff_2])
      abjad> pitchtools.diatonicize(score)
      abjad> f(score)
         \new Score <<
                 \new Staff {
                         \times 4/3 {
                                 c'8
                                 d'8
                                 e'8
                         }
                 }
                 \new Staff {
                         f'8
                         g'8
                         a'8
                         b'8
                 }
         >>
      abjad> leaftools.get_composite_offset_difference_series(score)
      [Rational(1, 8), Rational(1, 24), Rational(1, 12), Rational(1, 12), Rational(1, 24), Rational(1, 8)]
   '''

   return list(listtools.difference_series(get_composite_offset_series(expr)))
