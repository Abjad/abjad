# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TreeNode_proper_parentage_01():

    leaf = datastructuretools.TreeNode()
    subsubcontainer = datastructuretools.TreeContainer()
    subcontainer = datastructuretools.TreeContainer()
    container = datastructuretools.TreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.proper_parentage == (subsubcontainer, subcontainer, container)
    assert subsubcontainer.proper_parentage == (subcontainer, container)
    assert subcontainer.proper_parentage == (container,)
    assert container.proper_parentage == ()
