# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_rhythmtreetools_RhythmTreeNode_parent_01():

    leaf = rhythmtreetools.RhythmTreeLeaf()
    container = rhythmtreetools.RhythmTreeContainer()
    subcontainer = rhythmtreetools.RhythmTreeContainer()

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
