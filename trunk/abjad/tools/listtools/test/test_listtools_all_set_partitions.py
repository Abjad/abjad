from abjad import *


def test_listtools_all_set_partitions_01( ):

   l = [1, 2, 3, 4]
   set_partitions = listtools.all_set_partitions(l)

   assert set_partitions.next( ) == [[1, 2, 3, 4]]
   assert set_partitions.next( ) == [[1, 2, 3], [4]]
   assert set_partitions.next( ) == [[1, 2, 4], [3]]
   assert set_partitions.next( ) == [[1, 2], [3, 4]]
   assert set_partitions.next( ) == [[1, 2], [3], [4]]
   assert set_partitions.next( ) == [[1, 3, 4], [2]]
   assert set_partitions.next( ) == [[1, 3], [2, 4]]
   assert set_partitions.next( ) == [[1, 3], [2], [4]]
   assert set_partitions.next( ) == [[1, 4], [2, 3]]
   assert set_partitions.next( ) == [[1], [2, 3, 4]]
   assert set_partitions.next( ) == [[1], [2, 3], [4]]
   assert set_partitions.next( ) == [[1, 4], [2], [3]]
   assert set_partitions.next( ) == [[1], [2, 4], [3]]
   assert set_partitions.next( ) == [[1], [2], [3, 4]]
   assert set_partitions.next( ) == [[1], [2], [3], [4]]
