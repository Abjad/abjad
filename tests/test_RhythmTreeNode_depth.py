import abjad
import abjad.rhythmtrees


def test_RhythmTreeNode_depth_01():

    container = abjad.rhythmtrees.RhythmTreeContainer()
    assert container.depth == 0

    leaf = abjad.rhythmtrees.RhythmTreeLeaf()
    assert leaf.depth == 0

    container.append(leaf)
    assert leaf.depth == 1

    subcontainer = abjad.rhythmtrees.RhythmTreeContainer()
    assert subcontainer.depth == 0

    container.append(subcontainer)
    assert subcontainer.depth == 1

    subcontainer.append(leaf)
    assert leaf.depth == 2

    subsubcontainer = abjad.rhythmtrees.RhythmTreeContainer()
    assert subsubcontainer.depth == 0

    subcontainer.append(subsubcontainer)
    assert subsubcontainer.depth == 2

    subsubcontainer.append(leaf)
    assert leaf.depth == 3
