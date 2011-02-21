from abjad import *


def test_seqtools_partition_sequence_by_ratio_of_lengths_01( ):

   parts = seqtools.partition_sequence_by_ratio_of_lengths(range(10), [1, 1, 2])
   assert parts == [[0, 1, 2], [3, 4], [5, 6, 7, 8, 9]]
