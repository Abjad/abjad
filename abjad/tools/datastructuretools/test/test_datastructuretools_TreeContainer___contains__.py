# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer___contains___01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()

    subcontainer = datastructuretools.TreeContainer([leaf_b])

    container = datastructuretools.TreeContainer([leaf_a, subcontainer])

    assert leaf_a in container
    assert leaf_b not in container
    assert leaf_c not in container
