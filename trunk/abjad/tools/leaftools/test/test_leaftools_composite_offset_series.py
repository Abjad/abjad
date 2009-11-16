from abjad import *


def test_leaftools_composite_offset_series_01( ):

   staff_1 = Staff(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
   staff_2 = Staff(construct.run(4))
   score = Score([staff_1, staff_2])
   pitchtools.diatonicize(score)

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

   result = leaftools.composite_offset_series(score)
   assert result == [Rational(0, 1), Rational(1, 12), Rational(1, 8), Rational(1, 6), Rational(1, 4), Rational(1, 3), Rational(3, 8), Rational(5, 12), Rational(1, 2)]
