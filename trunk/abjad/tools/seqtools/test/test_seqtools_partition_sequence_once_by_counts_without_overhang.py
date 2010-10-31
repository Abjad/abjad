from abjad import *


def test_seqtools_partition_sequence_once_by_counts_without_overhang_01( ):
   '''Partition list.
   '''

   l = range(16)
   parts = seqtools.partition_sequence_once_by_counts_without_overhang(l, [4, 6]) 

   "[[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]"

   assert len(parts) == 2
   assert parts[0] == [0, 1, 2, 3]
   assert parts[1] == [4, 5, 6, 7, 8, 9]


def test_seqtools_partition_sequence_once_by_counts_without_overhang_02( ):
   '''Partition Abjad container..
   '''

   container = Container(macros.scale(6))
   parts = seqtools.partition_sequence_once_by_counts_without_overhang(container, [1, 2])

   "[{c'8}, {d'8, e'8}]"

   assert len(parts) == 2
   assert parts[0] == Container("c'8")
   assert parts[0][0] is not container[0]
   assert parts[1] == Container("d'8 e'8")
   assert parts[1][0] is not container[1]
   assert parts[1][1] is not container[2]
