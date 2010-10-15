from abjad import *


def test_Skip___init____01( ):
   '''Init skip from LilyPond input string.
   '''

   skip = skiptools.Skip('s8.')
   assert isinstance(skip, skiptools.Skip)


def test_Skip___init____02( ):
   '''Init skip from written duration and LilyPond multiplier.
   '''

   skip = skiptools.Skip((1, 4), (1, 2))

   assert isinstance(skip, skiptools.Skip)
