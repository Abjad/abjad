from abjad import rhythmtree


def test_RhythmTreeNode_root_01():

    leaf = rhythmtree.RhythmTreeLeaf()
    subsubcontainer = rhythmtree.RhythmTreeContainer()
    subcontainer = rhythmtree.RhythmTreeContainer()
    container = rhythmtree.RhythmTreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.root is container
    assert subsubcontainer.root is container
    assert subcontainer.root is container
    assert container.root is None
