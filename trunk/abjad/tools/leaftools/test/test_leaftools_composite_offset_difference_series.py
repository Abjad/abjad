from abjad import *


def test_leaftools_composite_offset_difference_series_01( ):

   staff_1 = Staff([FixedDurationTuplet((4, 8), construct.run(3))])
   staff_2 = Staff(construct.run(4))
   score = Score([staff_1, staff_2])
   pitchtools.diatonicize(score)

   r'''
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
   '''

   result = leaftools.composite_offset_difference_series(score)
   assert result == [Rational(1, 8), Rational(1, 24), Rational(1, 12), Rational(1, 12), Rational(1, 24), Rational(1, 8)]
