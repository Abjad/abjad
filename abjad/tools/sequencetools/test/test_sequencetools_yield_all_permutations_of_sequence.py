# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_permutations_of_sequence_01():
    r'''Yield all permtuations of tuple.
    '''

    sequence = (1, 2, 3)
    generator = sequencetools.yield_all_permutations_of_sequence(sequence)
    permutations = list(generator)
    assert permutations == [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]


# TODO: remove this functionality
def test_sequencetools_yield_all_permutations_of_sequence_02():
    r'''Yield all permtuations of Abjad container.
    '''

    container = Container("c'8 d'8 e'8")
    generator = sequencetools.yield_all_permutations_of_sequence(container)
    permutations = list(generator)
    assert str(permutations) == '[Container("c\'8 d\'8 e\'8"), Container("c\'8 e\'8 d\'8"), Container("d\'8 c\'8 e\'8"), Container("d\'8 e\'8 c\'8"), Container("e\'8 c\'8 d\'8"), Container("e\'8 d\'8 c\'8")]'
