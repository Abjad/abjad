from abjad.tools.durationtools import Duration
from abjad.tools.rhythmtreetools import RhythmTreeContainer, RhythmTreeLeaf


def test_RhythmTreeNode_prolated_duration_01():

    tree = RhythmTreeContainer(1, [
        RhythmTreeLeaf(1),
        RhythmTreeContainer(2, [
            RhythmTreeLeaf(3),
            RhythmTreeLeaf(2)
        ]),
        RhythmTreeLeaf(2)
    ])

    assert tree.prolated_duration == Duration(1)
    assert tree[0].prolated_duration == Duration(1, 5)
    assert tree[1].prolated_duration == Duration(2, 5)
    assert tree[1][0].prolated_duration == Duration(6, 25)
    assert tree[1][1].prolated_duration == Duration(4, 25)
    assert tree[2].prolated_duration == Duration(2, 5)

    tree[1].append(tree.pop())

    assert tree.prolated_duration == Duration(1)
    assert tree[0].prolated_duration == Duration(1, 3)
    assert tree[1].prolated_duration == Duration(2, 3)
    assert tree[1][0].prolated_duration == Duration(2, 7)
    assert tree[1][1].prolated_duration == Duration(4, 21)
    assert tree[1][2].prolated_duration == Duration(4, 21)

    tree.duration = 19

    assert tree.prolated_duration == Duration(19)
    assert tree[0].prolated_duration == Duration(19, 3)
    assert tree[1].prolated_duration == Duration(38, 3)
    assert tree[1][0].prolated_duration == Duration(38, 7)
    assert tree[1][1].prolated_duration == Duration(76, 21)
    assert tree[1][2].prolated_duration == Duration(76, 21)
