import abjad
from abjad.tools import rhythmtreetools


def test_rhythmtreetools_RhythmTreeNode_offset_01():

    tree = rhythmtreetools.RhythmTreeContainer(preprolated_duration=1, children=[
        rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1),
        rhythmtreetools.RhythmTreeContainer(preprolated_duration=2, children=[
            rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3),
            rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
        ]),
        rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
    ])

    assert tree.start_offset == abjad.Offset(0)
    assert tree[0].start_offset == abjad.Offset(0)
    assert tree[1].start_offset == abjad.Offset(1, 5)
    assert tree[1][0].start_offset == abjad.Offset(1, 5)
    assert tree[1][1].start_offset == abjad.Offset(11, 25)
    assert tree[2].start_offset == abjad.Offset(3, 5)

    node = tree.pop()

    assert node.start_offset == abjad.Offset(0)

    tree[1].append(node)

    assert tree.start_offset == abjad.Offset(0)
    assert tree[0].start_offset == abjad.Offset(0)
    assert tree[1].start_offset == abjad.Offset(1, 3)
    assert tree[1][0].start_offset == abjad.Offset(1, 3)
    assert tree[1][1].start_offset == abjad.Offset(13, 21)
    assert tree[1][2].start_offset == abjad.Offset(17, 21)

    tree.preprolated_duration = 19

    assert tree.start_offset == abjad.Offset(0)
    assert tree[0].start_offset == abjad.Offset(0)
    assert tree[1].start_offset == abjad.Offset(19, 3)
    assert tree[1][0].start_offset == abjad.Offset(19, 3)
    assert tree[1][1].start_offset == abjad.Offset(247, 21)
    assert tree[1][2].start_offset == abjad.Offset(323, 21)
