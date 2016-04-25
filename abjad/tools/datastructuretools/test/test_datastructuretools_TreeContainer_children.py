# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer_children_01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()
    subcontainer = datastructuretools.TreeContainer([leaf_b, leaf_c])
    leaf_d = datastructuretools.TreeNode()

    container = datastructuretools.TreeContainer([leaf_a, subcontainer, leaf_d])

    assert container.children == (leaf_a, subcontainer, leaf_d)
