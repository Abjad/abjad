# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeNode_depth_01():

    container = datastructuretools.TreeContainer()
    assert container.depth == 0

    leaf = datastructuretools.TreeNode()
    assert leaf.depth == 0

    container.append(leaf)
    assert leaf.depth == 1

    subcontainer = datastructuretools.TreeContainer()
    assert subcontainer.depth == 0

    container.append(subcontainer)
    assert subcontainer.depth == 1

    subcontainer.append(leaf)
    assert leaf.depth == 2

    subsubcontainer = datastructuretools.TreeContainer()
    assert subsubcontainer.depth == 0

    subcontainer.append(subsubcontainer)
    assert subsubcontainer.depth == 2

    subsubcontainer.append(leaf)
    assert leaf.depth == 3
