# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeNode_depth_01():

    container = rhythmtreetools.RhythmTreeContainer()
    assert container.depth == 0

    leaf = rhythmtreetools.RhythmTreeLeaf()
    assert leaf.depth == 0

    container.append(leaf)
    assert leaf.depth == 1

    subcontainer = rhythmtreetools.RhythmTreeContainer()
    assert subcontainer.depth == 0

    container.append(subcontainer)
    assert subcontainer.depth == 1

    subcontainer.append(leaf)
    assert leaf.depth == 2

    subsubcontainer = rhythmtreetools.RhythmTreeContainer()
    assert subsubcontainer.depth == 0

    subcontainer.append(subsubcontainer)
    assert subsubcontainer.depth == 2

    subsubcontainer.append(leaf)
    assert leaf.depth == 3
