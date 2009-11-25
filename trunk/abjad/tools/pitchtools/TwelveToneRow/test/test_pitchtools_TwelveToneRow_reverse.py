from abjad import *


def test_pitchtools_TwelveToneRow_reverse_01( ):

   row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
   reverse = pitchtools.TwelveToneRow([11, 4, 9, 1, 3, 5, 7, 8, 6, 2, 0, 10])

   assert row.reverse( ) == reverse
