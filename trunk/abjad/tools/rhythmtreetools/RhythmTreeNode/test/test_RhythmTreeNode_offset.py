from abjad.tools.durationtools import Offset
from abjad.tools.rhythmtreetools import RhythmTreeContainer, RhythmTreeLeaf


def test_RhythmTreeNode_offset_01():

    tree = RhythmTreeContainer(1, [
        RhythmTreeLeaf(1),
        RhythmTreeContainer(2, [
            RhythmTreeLeaf(3),
            RhythmTreeLeaf(2)
        ]),
        RhythmTreeLeaf(2)
    ])

    assert tree.offset == Offset(0)
    assert tree[0].offset == Offset(0)
    assert tree[1].offset == Offset(1, 5)
    assert tree[1][0].offset == Offset(1, 5)
    assert tree[1][1].offset == Offset(11, 25)
    assert tree[2].offset == Offset(3, 5)

    node = tree.pop()

    assert node.offset == Offset(0)

    tree[1].append(node)

    assert tree.offset == Offset(0)
    assert tree[0].offset == Offset(0)
    assert tree[1].offset == Offset(1, 3)
    assert tree[1][0].offset == Offset(1, 3)
    assert tree[1][1].offset == Offset(13, 21)
    assert tree[1][2].offset == Offset(17, 21)
    
    tree.duration = 19
        
    assert tree.offset == Offset(0)
    assert tree[0].offset == Offset(0)
    assert tree[1].offset == Offset(19, 3)
    assert tree[1][0].offset == Offset(19, 3)
    assert tree[1][1].offset == Offset(247, 21)
    assert tree[1][2].offset == Offset(323, 21)

