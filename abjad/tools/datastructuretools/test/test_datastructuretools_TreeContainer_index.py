# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_datastructuretools_TreeContainer_index_01():

    leaf_a = datastructuretools.TreeNode()
    leaf_b = datastructuretools.TreeNode()
    leaf_c = datastructuretools.TreeNode()
    subcontainer = datastructuretools.TreeContainer([leaf_b, leaf_c])
    leaf_d = datastructuretools.TreeNode()
    container = datastructuretools.TreeContainer([
        leaf_a,
        subcontainer,
        leaf_d,
        ])

    assert container.index(leaf_a) == 0
    assert container.index(subcontainer) == 1
    assert container.index(leaf_d) == 2

    pytest.raises(ValueError, 'container.index(leaf_b)')
    pytest.raises(ValueError, 'container.index(leaf_c)')
