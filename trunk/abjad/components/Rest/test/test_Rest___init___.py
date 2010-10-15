from abjad import *


def test_Rest___init____01( ):
   '''Init rest from LilyPond input string.
   '''

   rest = Rest('r8.')
   
   assert rest.duration.written == Fraction(3, 16)


def test_Rest___init____02( ):
   '''Init rest from written duration and LilyPond multiplier.
   '''

   rest = Rest(Fraction(1, 4), Fraction(1, 2))

   assert rest.format == 'r4 * 1/2'
