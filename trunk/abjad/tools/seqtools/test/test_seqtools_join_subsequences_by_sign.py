from abjad import *


def test_seqtools_join_subsequences_by_sign_01( ):

   l = [[1, 2], [3, 4], [-5, -6, -7], [-8, -9, -10], [11, 12]]
   t = seqtools.join_subsequences_by_sign(l)

   assert t == [[1, 2, 3, 4], [-5, -6, -7, -8, -9, -10], [11, 12]]


def test_seqtools_join_subsequences_by_sign_02( ):

   l = [[1, 2], [ ], [ ], [3, 4, 5], [6, 7]]
   t = seqtools.join_subsequences_by_sign(l)

   assert t == [[1, 2], [ ], [3, 4, 5, 6, 7]]
