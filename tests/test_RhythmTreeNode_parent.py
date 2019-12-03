import pytest

import abjad.rhythmtrees


def test_RhythmTreeNode_parent_01():

    leaf = abjad.rhythmtrees.RhythmTreeLeaf()
    container = abjad.rhythmtrees.RhythmTreeContainer()
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer()

    assert leaf.parent is None
    assert container.parent is None
    assert subcontainer.parent is None

    container.append(leaf)
    assert leaf.parent is container

    container.append(subcontainer)
    assert subcontainer.parent is container
    assert leaf.parent is container
    assert container.parent is None

    subcontainer.append(leaf)
    assert leaf.parent is subcontainer
    assert subcontainer.parent is container
    assert container.parent is None

    with pytest.raises(ValueError):
        subcontainer.append(container)
