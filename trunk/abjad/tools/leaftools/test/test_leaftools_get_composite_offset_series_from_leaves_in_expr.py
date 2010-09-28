from abjad import *


def test_leaftools_get_composite_offset_series_from_leaves_in_expr_01( ):

   staff_1 = Staff(tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
   staff_2 = Staff(notetools.make_repeated_notes(4))
   score = Score([staff_1, staff_2])
   macros.diatonicize(score)

   r'''
   \new Score <<
           \new Staff {
                   \times 2/3 {
                           c'8
                           d'8
                           e'8
                   }
                   \times 2/3 {
                           f'8
                           g'8
                           a'8
                   }
           }
           \new Staff {
                   b'8
                   c''8
                   d''8
                   e''8
           }
   >>
   '''

   result = leaftools.get_composite_offset_series_from_leaves_in_expr(score)
   assert result == [Fraction(0, 1), Fraction(1, 12), Fraction(1, 8), Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(3, 8), Fraction(5, 12), Fraction(1, 2)]
