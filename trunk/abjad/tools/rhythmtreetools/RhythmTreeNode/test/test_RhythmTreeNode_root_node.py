from abjad import *


def test_RhythmTreeNode_root_node_01():

    leaf = rhythmtreetools.RhythmTreeLeaf()
    subsubcontainer = rhythmtreetools.RhythmTreeContainer()
    subcontainer = rhythmtreetools.RhythmTreeContainer()
    container = rhythmtreetools.RhythmTreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.root_node == container
    assert subsubcontainer.root_node == container
    assert subcontainer.root_node == container
    assert container.root_node == container
