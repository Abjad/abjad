from abjad import *


def test_Rest___init____01( ):
   '''Init rest from LilyPond input string.
   '''

   rest = Rest('r8.')
   
   assert rest.duration.written == Fraction(3, 16)
