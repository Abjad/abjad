# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_datastructuretools_TreeNode_parent_01():

    leaf = datastructuretools.TreeNode()
    container = datastructuretools.TreeContainer()
    subcontainer = datastructuretools.TreeContainer()

    assert leaf.parent is None
    assert container.parent is None
    assert subcontainer.parent is None

    container.append(leaf)
    assert leaf.parent is container

    container.append(subcontainer)
    assert subcontainer.parent is container
    assert leaf.parent is container
    assert container.parent is None

    subcontainer.append(leaf)
    assert leaf.parent is subcontainer
    assert subcontainer.parent is container
    assert container.parent is None

    pytest.raises(AssertionError, 'subcontainer.append(container)')
