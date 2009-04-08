from abjad import *


def test_in_terms_of_01( ):
   assert mathtools.in_terms_of((0, 6), 12) == (0, 12)
   assert mathtools.in_terms_of((1, 6), 12) == (2, 12)
   assert mathtools.in_terms_of((2, 6), 12) == (4, 12)
   assert mathtools.in_terms_of((3, 6), 12) == (6, 12)
   assert mathtools.in_terms_of((4, 6), 12) == (8, 12)
   assert mathtools.in_terms_of((5, 6), 12) == (10, 12)
   assert mathtools.in_terms_of((6, 6), 12) == (12, 12)
   assert mathtools.in_terms_of((7, 6), 12) == (14, 12)
   assert mathtools.in_terms_of((8, 6), 12) == (16, 12)
   assert mathtools.in_terms_of((9, 6), 12) == (18, 12)
   assert mathtools.in_terms_of((10, 6), 12) == (20, 12)
   assert mathtools.in_terms_of((11, 6), 12) == (22, 12)


def test_in_terms_of_02( ):
   assert mathtools.in_terms_of((0, 12), 6) == (0, 6)
   assert mathtools.in_terms_of((1, 12), 6) == (1, 12)
   assert mathtools.in_terms_of((2, 12), 6) == (1, 6)
   assert mathtools.in_terms_of((3, 12), 6) == (3, 12)
   assert mathtools.in_terms_of((4, 12), 6) == (2, 6)
   assert mathtools.in_terms_of((5, 12), 6) == (5, 12)
   assert mathtools.in_terms_of((6, 12), 6) == (3, 6)
   assert mathtools.in_terms_of((7, 12), 6) == (7, 12)
   assert mathtools.in_terms_of((8, 12), 6) == (4, 6)
   assert mathtools.in_terms_of((9, 12), 6) == (9, 12)
   assert mathtools.in_terms_of((10, 12), 6) == (5, 6)
   assert mathtools.in_terms_of((11, 12), 6) == (11, 12)


def test_in_terms_of_03( ):
   assert mathtools.in_terms_of((0, 12), 8) == (0, 8)
   assert mathtools.in_terms_of((1, 12), 8) == (1, 12)
   assert mathtools.in_terms_of((2, 12), 8) == (2, 12)
   assert mathtools.in_terms_of((3, 12), 8) == (2, 8)
   assert mathtools.in_terms_of((4, 12), 8) == (4, 12)
   assert mathtools.in_terms_of((5, 12), 8) == (5, 12)
   assert mathtools.in_terms_of((6, 12), 8) == (4, 8)
   assert mathtools.in_terms_of((7, 12), 8) == (7, 12)
   assert mathtools.in_terms_of((8, 12), 8) == (8, 12)
   assert mathtools.in_terms_of((9, 12), 8) == (6, 8)
   assert mathtools.in_terms_of((10, 12), 8) == (10, 12)
   assert mathtools.in_terms_of((11, 12), 8) == (11, 12)
