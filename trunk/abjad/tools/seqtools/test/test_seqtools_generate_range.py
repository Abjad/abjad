from abjad import *


def test_seqtools_generate_range_01( ):
   '''Same arguments as built-in range.
   '''

   g = seqtools.generate_range(1, 8)
   
   assert list(g) == [1, 2, 3, 4, 5, 6, 7]
