from abjad import *


def test_listtools_partition_sequence_by_restricted_growth_function_01( ):

   l = range(10)
   rgf = [1, 1, 2, 2, 1, 2, 3, 3, 2, 4]
   partition = listtools.partition_sequence_by_restricted_growth_function(l, rgf)
   assert partition == [[0, 1, 4], [2, 3, 5, 8], [6, 7], [9]]
