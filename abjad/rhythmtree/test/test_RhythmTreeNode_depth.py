import abjad
from abjad import rhythmtree


def test_RhythmTreeNode_depth_01():

    container = rhythmtree.RhythmTreeContainer()
    assert container.depth == 0

    leaf = rhythmtree.RhythmTreeLeaf()
    assert leaf.depth == 0

    container.append(leaf)
    assert leaf.depth == 1

    subcontainer = rhythmtree.RhythmTreeContainer()
    assert subcontainer.depth == 0

    container.append(subcontainer)
    assert subcontainer.depth == 1

    subcontainer.append(leaf)
    assert leaf.depth == 2

    subsubcontainer = rhythmtree.RhythmTreeContainer()
    assert subsubcontainer.depth == 0

    subcontainer.append(subsubcontainer)
    assert subsubcontainer.depth == 2

    subsubcontainer.append(leaf)
    assert leaf.depth == 3
