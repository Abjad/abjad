# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer_remove_01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()

    container = datastructuretools.TreeContainer([leaf_a, leaf_b, leaf_c])
    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert leaf_a.parent is container
    assert leaf_b.parent is container
    assert leaf_c.parent is container

    container.remove(leaf_a)
    assert container.children == (leaf_b, leaf_c)
    assert leaf_a.parent is None

    container.remove(leaf_c)
    assert container.children == (leaf_b,)
    assert leaf_c.parent is None
