# -*- coding: utf-8 -*-
from abjad.tools.durationtools import Duration
from abjad.tools.rhythmtreetools import RhythmTreeContainer, RhythmTreeLeaf


def test_rhythmtreetools_RhythmTreeNode_duration_01():

    tree = RhythmTreeContainer(preprolated_duration=1, children=[
        RhythmTreeLeaf(preprolated_duration=1),
        RhythmTreeContainer(preprolated_duration=2, children=[
            RhythmTreeLeaf(preprolated_duration=3),
            RhythmTreeLeaf(preprolated_duration=2)
        ]),
        RhythmTreeLeaf(preprolated_duration=2)
    ])

    assert tree.duration == Duration(1)
    assert tree[0].duration == Duration(1, 5)
    assert tree[1].duration == Duration(2, 5)
    assert tree[1][0].duration == Duration(6, 25)
    assert tree[1][1].duration == Duration(4, 25)
    assert tree[2].duration == Duration(2, 5)

    tree[1].append(tree.pop())

    assert tree.duration == Duration(1)
    assert tree[0].duration == Duration(1, 3)
    assert tree[1].duration == Duration(2, 3)
    assert tree[1][0].duration == Duration(2, 7)
    assert tree[1][1].duration == Duration(4, 21)
    assert tree[1][2].duration == Duration(4, 21)

    tree.preprolated_duration = 19

    assert tree.duration == Duration(19)
    assert tree[0].duration == Duration(19, 3)
    assert tree[1].duration == Duration(38, 3)
    assert tree[1][0].duration == Duration(38, 7)
    assert tree[1][1].duration == Duration(76, 21)
    assert tree[1][2].duration == Duration(76, 21)
