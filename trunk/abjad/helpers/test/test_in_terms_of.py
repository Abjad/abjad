from abjad.helpers.in_terms_of import _in_terms_of
from abjad import *


def test_in_terms_of_01( ):
   assert _in_terms_of((0, 6), 12) == (0, 12)
   assert _in_terms_of((1, 6), 12) == (2, 12)
   assert _in_terms_of((2, 6), 12) == (4, 12)
   assert _in_terms_of((3, 6), 12) == (6, 12)
   assert _in_terms_of((4, 6), 12) == (8, 12)
   assert _in_terms_of((5, 6), 12) == (10, 12)
   assert _in_terms_of((6, 6), 12) == (12, 12)
   assert _in_terms_of((7, 6), 12) == (14, 12)
   assert _in_terms_of((8, 6), 12) == (16, 12)
   assert _in_terms_of((9, 6), 12) == (18, 12)
   assert _in_terms_of((10, 6), 12) == (20, 12)
   assert _in_terms_of((11, 6), 12) == (22, 12)
