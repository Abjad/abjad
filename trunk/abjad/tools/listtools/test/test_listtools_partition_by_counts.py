from abjad import *


def test_listtools_partition_by_counts_01( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   t = listtools.partition_by_counts(l, [3])
   assert t == [[0, 1, 2]]


def test_listtools_partition_by_counts_02( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   t = listtools.partition_by_counts(l, [3], cyclic = True) 
   assert t == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_listtools_partition_by_counts_03( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   t = listtools.partition_by_counts(l, [3], overhang = True)
   assert t == [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]


def test_listtools_partition_by_counts_04( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   t = listtools.partition_by_counts(l, [3], cyclic = True, overhang = True)
   assert t == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


def test_listtools_partition_by_counts_05( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
   t = listtools.partition_by_counts(l, [4, 3])
   assert t == [[0, 1, 2, 3], [4, 5, 6]]


def test_listtools_partition_by_counts_06( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
   t = listtools.partition_by_counts(l, [4, 3], cyclic = True)
   assert t == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]


def test_listtools_partition_by_counts_07( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
   t = listtools.partition_by_counts(l, [4, 3], overhang = True)
   assert t == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]


def test_listtools_partition_by_counts_08( ):
   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
   t = listtools.partition_by_counts(l, [4, 3], cyclic = True, overhang = True)
   assert t == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]
