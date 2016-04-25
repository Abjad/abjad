# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer___eq___01():

    tree_container_1 = datastructuretools.TreeContainer([])
    tree_container_2 = datastructuretools.TreeContainer([])

    assert format(tree_container_1) == format(tree_container_2)
    assert tree_container_1 != tree_container_2


def test_datastructuretools_TreeContainer___eq___02():

    tree_container_1 = datastructuretools.TreeContainer([
        datastructuretools.TreeNode()
        ])
    tree_container_2 = datastructuretools.TreeContainer([
        datastructuretools.TreeNode()
        ])

    assert format(tree_container_1) == format(tree_container_2)
    assert tree_container_1 != tree_container_2


def test_datastructuretools_TreeContainer___eq___03():

    tree_container_1 = datastructuretools.TreeContainer([])
    tree_container_2 = datastructuretools.TreeContainer([
        datastructuretools.TreeNode()
        ])
    tree_container_3 = datastructuretools.TreeContainer([
        datastructuretools.TreeNode(),
        datastructuretools.TreeNode()
        ])

    assert format(tree_container_1) != format(tree_container_2)
    assert tree_container_1 != tree_container_2
    assert tree_container_1 != tree_container_3
    assert tree_container_2 != tree_container_3
