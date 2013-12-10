# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_PayloadTree_to_nested_lists_01():

    sequence_1 = [[0, 1], [2, 3]]
    tree_1 = datastructuretools.PayloadTree(sequence_1)

    sequence_2 = tree_1.to_nested_lists()
    tree_2 = datastructuretools.PayloadTree(sequence_2)

    assert isinstance(sequence_2, list)
    assert sequence_1 == sequence_2
    assert tree_1 == tree_2
