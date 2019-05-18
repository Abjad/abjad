import abjad
import abjad.rhythmtrees


def test_RhythmTreeNode_duration_01():

    tree = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1,
        children=[
            abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1),
            abjad.rhythmtrees.RhythmTreeContainer(
                preprolated_duration=2,
                children=[
                    abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3),
                    abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2),
                ],
            ),
            abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2),
        ],
    )

    assert tree.duration == abjad.Duration(1)
    assert tree[0].duration == abjad.Duration(1, 5)
    assert tree[1].duration == abjad.Duration(2, 5)
    assert tree[1][0].duration == abjad.Duration(6, 25)
    assert tree[1][1].duration == abjad.Duration(4, 25)
    assert tree[2].duration == abjad.Duration(2, 5)

    tree[1].append(tree.pop())

    assert tree.duration == abjad.Duration(1)
    assert tree[0].duration == abjad.Duration(1, 3)
    assert tree[1].duration == abjad.Duration(2, 3)
    assert tree[1][0].duration == abjad.Duration(2, 7)
    assert tree[1][1].duration == abjad.Duration(4, 21)
    assert tree[1][2].duration == abjad.Duration(4, 21)

    tree.preprolated_duration = 19

    assert tree.duration == abjad.Duration(19)
    assert tree[0].duration == abjad.Duration(19, 3)
    assert tree[1].duration == abjad.Duration(38, 3)
    assert tree[1][0].duration == abjad.Duration(38, 7)
    assert tree[1][1].duration == abjad.Duration(76, 21)
    assert tree[1][2].duration == abjad.Duration(76, 21)
