from abjad import *
from abjad.tools import seqtools


def test_seqtools_partition_sequence_extended_to_counts_without_overhang_01( ):

   parts = seqtools.partition_sequence_extended_to_counts_without_overhang([1, 2, 3, 4], [6, 6, 6])


   assert parts == [[1, 2, 3, 4, 1, 2], [3, 4, 1, 2, 3, 4], [1, 2, 3, 4, 1, 2]]
