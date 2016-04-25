# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer_insert_01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()

    container = datastructuretools.TreeContainer()
    assert container.children == ()

    container.insert(0, leaf_a)
    assert container.children == (leaf_a,)

    container.insert(0, leaf_b)
    assert container.children == (leaf_b, leaf_a)

    container.insert(1, leaf_c)
    assert container.children == (leaf_b, leaf_c, leaf_a)
