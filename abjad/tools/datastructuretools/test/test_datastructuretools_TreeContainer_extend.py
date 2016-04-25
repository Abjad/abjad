# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer_extend_01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()
    leaf_d = datastructuretools.TreeNode()

    container = datastructuretools.TreeContainer()

    assert container.children == ()

    container.extend([leaf_a])
    assert container.children == (leaf_a,)

    container.extend([leaf_b, leaf_c, leaf_d])
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)

    container.extend([leaf_a, leaf_c])
    assert container.children == (leaf_b, leaf_d, leaf_a, leaf_c)
