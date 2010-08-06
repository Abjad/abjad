from abjad.tools import listtools
from abjad.tools.leaftools.get_composite_offset_series_from_leaves_in_expr import \
   get_composite_offset_series_from_leaves_in_expr


def get_composite_offset_difference_series_from_leaves_in_expr(expr):
   r'''.. versionadded:: 1.1.2

   List time intervals between unique start and stop offsets 
   of `expr` leaves::

      abjad> staff_1 = Staff([FixedDurationTuplet((4, 8), leaftools.make_repeated_notes(3))])
      abjad> staff_2 = Staff(leaftools.make_repeated_notes(4))
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
      abjad> leaftools.get_composite_offset_difference_series_from_leaves_in_expr(score)
      [Rational(1, 8), Rational(1, 24), Rational(1, 12), Rational(1, 12), Rational(1, 24), Rational(1, 8)]

   .. versionchanged:: 1.1.2
      renamed ``leaftools.get_composite_offset_difference_series( )`` to
      ``leaftools.get_composite_offset_difference_series_from_leaves_in_expr( )``.
   '''

   return list(listtools.difference_series(get_composite_offset_series_from_leaves_in_expr(expr)))
