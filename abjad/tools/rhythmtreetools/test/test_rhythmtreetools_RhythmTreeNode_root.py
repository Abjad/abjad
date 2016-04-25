# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeNode_root_01():

    leaf = rhythmtreetools.RhythmTreeLeaf()
    subsubcontainer = rhythmtreetools.RhythmTreeContainer()
    subcontainer = rhythmtreetools.RhythmTreeContainer()
    container = rhythmtreetools.RhythmTreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.root == container
    assert subsubcontainer.root == container
    assert subcontainer.root == container
    assert container.root == container
