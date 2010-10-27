from abjad import *


def test_listtools_yield_all_rotations_of_sequence_01( ):
   '''Yield all rotations of list.
   '''

   rotations = list(listtools.yield_all_rotations_of_sequence([1, 2, 3, 4], -1))
   assert rotations == [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]


def test_listtools_yield_all_rotations_of_sequence_02( ):
   '''Yield all rotations of tuple.
   '''

   rotations = list(listtools.yield_all_rotations_of_sequence((1, 2, 3, 4), -1))
   assert rotations == [(1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, 3)]


def test_listtools_yield_all_rotations_of_sequence_03( ):
   '''Yield all rotations of Abjad container.
   '''

   container = Container("c'8 d'8 e'8")
   #rotations = list(listtools.yield_all_rotations_of_sequence(container, -1))
   pass
