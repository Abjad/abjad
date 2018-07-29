import abjad.rhythmtrees


def test_RhythmTreeNode_root_01():

    leaf = abjad.rhythmtrees.RhythmTreeLeaf()
    subsubcontainer = abjad.rhythmtrees.RhythmTreeContainer()
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer()
    container = abjad.rhythmtrees.RhythmTreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.root is container
    assert subsubcontainer.root is container
    assert subcontainer.root is container
    assert container.root is None
