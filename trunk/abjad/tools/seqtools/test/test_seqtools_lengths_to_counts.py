from abjad import *


def test_seqtools_lengths_to_counts_01( ):

   t = seqtools.lengths_to_counts([1, 2, -3, -4, 5])

   assert t == [[1], [2, 3], [-4, -5, -6], [-7, -8, -9, -10], [11, 12, 13, 14, 15]]


def test_seqtools_lengths_to_counts_02( ):

   t = seqtools.lengths_to_counts([1, 0, -3, -4, 5])

   assert t == [[1], [ ], [-2, -3, -4], [-5, -6, -7, -8], [9, 10, 11, 12, 13]]
