# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeNode_proper_parentage_01():

    leaf = rhythmtreetools.RhythmTreeLeaf()
    subsubcontainer = rhythmtreetools.RhythmTreeContainer()
    subcontainer = rhythmtreetools.RhythmTreeContainer()
    container = rhythmtreetools.RhythmTreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.proper_parentage == (subsubcontainer, subcontainer, container)
    assert subsubcontainer.proper_parentage == (subcontainer, container)
    assert subcontainer.proper_parentage == (container,)
    assert container.proper_parentage == ()
