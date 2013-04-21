from abjad import *


def test_Tree___init___01():
    '''Initialize tree from other tree.
    '''

    tree_1 = sequencetools.Tree([[4, 5], [6, 7]])
    tree_2 = sequencetools.Tree(tree_1)

    assert tree_1 is not tree_2
    assert tree_1 == tree_2
