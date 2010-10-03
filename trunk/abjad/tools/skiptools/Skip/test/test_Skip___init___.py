from abjad import *
from abjad.tools.skiptools import Skip


def test_Skip___init____01( ):
   '''Init skip from LilyPond input string.
   '''

   skip = Skip('s8.')

   assert skip.duration.written == Fraction(3, 16)
