from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_Tree_to_nested_lists_01():

    sequence_1 = [[0, 1], [2, 3]]
    tree_1 = sequencetools.Tree(sequence_1)

    sequence_2 = tree_1.to_nested_lists()
    tree_2 = sequencetools.Tree(sequence_2)

    assert isinstance(sequence_2, list)
    assert sequence_1 == sequence_2
    assert tree_1 == tree_2
