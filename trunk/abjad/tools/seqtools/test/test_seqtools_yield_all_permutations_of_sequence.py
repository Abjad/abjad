from abjad import *


def test_seqtools_yield_all_permutations_of_sequence_01( ):
   '''Yield all permtuations of tuple.
   '''
   
   sequence = (1, 2, 3)
   generator = seqtools.yield_all_permutations_of_sequence(sequence)
   permutations = list(generator)
   assert permutations == [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]


def test_seqtools_yield_all_permutations_of_sequence_02( ):
   '''Yield all permtuations of Abjad container.
   '''
   
   container = Container("c'8 d'8 e'8")
   generator = seqtools.yield_all_permutations_of_sequence(container)
   permutations = list(generator)
   assert str(permutations) == "[{c'8, d'8, e'8}, {c'8, e'8, d'8}, {d'8, c'8, e'8}, {d'8, e'8, c'8}, {e'8, c'8, d'8}, {e'8, d'8, c'8}]"
