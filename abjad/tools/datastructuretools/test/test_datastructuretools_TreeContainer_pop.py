# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer_pop_01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()

    container = datastructuretools.TreeContainer([leaf_a, leaf_b, leaf_c])
    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert leaf_a.parent is container
    assert leaf_b.parent is container
    assert leaf_c.parent is container

    result = container.pop()
    assert container.children == (leaf_a, leaf_b)
    assert result is leaf_c
    assert result.parent is None

    result = container.pop(0)
    assert container.children == (leaf_b,)
    assert result is leaf_a
    assert result.parent is None
