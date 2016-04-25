# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeNode_root_01():

    leaf = datastructuretools.TreeNode()
    subsubcontainer = datastructuretools.TreeContainer()
    subcontainer = datastructuretools.TreeContainer()
    container = datastructuretools.TreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.root == container
    assert subsubcontainer.root == container
    assert subcontainer.root == container
    assert container.root == container
