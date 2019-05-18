import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer___eq___01():

    a = abjad.rhythmtrees.RhythmTreeContainer(children=[])
    b = abjad.rhythmtrees.RhythmTreeContainer(children=[])

    assert format(a) == format(b)
    assert a != b


def test_RhythmTreeContainer___eq___02():

    a = abjad.rhythmtrees.RhythmTreeContainer(
        children=[abjad.rhythmtrees.RhythmTreeLeaf()]
    )
    b = abjad.rhythmtrees.RhythmTreeContainer(
        children=[abjad.rhythmtrees.RhythmTreeLeaf()]
    )

    assert format(a) == format(b)
    assert a != b


def test_RhythmTreeContainer___eq___03():

    a = abjad.rhythmtrees.RhythmTreeContainer(children=[])
    b = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=2, children=[]
    )
    c = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1,
        children=[abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)],
    )
    d = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=2,
        children=[abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)],
    )
    e = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=2,
        children=[abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)],
    )

    assert a != b
    assert a != c
    assert a != d
    assert a != e
    assert b != c
    assert b != d
    assert b != e
    assert c != d
    assert c != e
    assert d != e
