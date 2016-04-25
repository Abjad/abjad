# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeNode_improper_parentage_01():

    container = rhythmtreetools.RhythmTreeContainer()
    assert container.improper_parentage == (container,)

    leaf = rhythmtreetools.RhythmTreeLeaf()
    assert leaf.improper_parentage == (leaf,)

    container.append(leaf)
    assert leaf.improper_parentage == (leaf, container)

    subcontainer = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf])
    container.append(subcontainer)
    assert leaf.improper_parentage == (leaf, subcontainer, container)
