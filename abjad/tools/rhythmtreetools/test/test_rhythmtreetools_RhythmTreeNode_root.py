from abjad.tools import rhythmtreetools


def test_rhythmtreetools_RhythmTreeNode_root_01():

    leaf = rhythmtreetools.RhythmTreeLeaf()
    subsubcontainer = rhythmtreetools.RhythmTreeContainer()
    subcontainer = rhythmtreetools.RhythmTreeContainer()
    container = rhythmtreetools.RhythmTreeContainer()

    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(leaf)

    assert leaf.root is container
    assert subsubcontainer.root is container
    assert subcontainer.root is container
    assert container.root is None
