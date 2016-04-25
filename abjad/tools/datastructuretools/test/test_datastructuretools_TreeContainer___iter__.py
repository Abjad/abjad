# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeContainer___iter___01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()

    container = datastructuretools.TreeContainer([leaf_a, leaf_b, leaf_c])

    assert [x for x in container] == [leaf_a, leaf_b, leaf_c]
