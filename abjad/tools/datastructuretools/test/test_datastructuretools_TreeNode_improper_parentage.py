# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeNode_improper_parentage_01():

    container = datastructuretools.TreeContainer()
    assert container.improper_parentage == (container,)

    leaf = datastructuretools.TreeNode()
    assert leaf.improper_parentage == (leaf,)

    container.append(leaf)
    assert leaf.improper_parentage == (leaf, container)

    subcontainer = datastructuretools.TreeContainer([leaf])
    container.append(subcontainer)
    assert leaf.improper_parentage == (leaf, subcontainer, container)
