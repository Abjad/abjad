import abjad
from abjad import rhythmtree


def test_RhythmTreeContainer___eq___01():

    a = rhythmtree.RhythmTreeContainer(children=[])
    b = rhythmtree.RhythmTreeContainer(children=[])

    assert format(a) == format(b)
    assert a != b


def test_RhythmTreeContainer___eq___02():

    a = rhythmtree.RhythmTreeContainer(children=[
        rhythmtree.RhythmTreeLeaf()
        ])
    b = rhythmtree.RhythmTreeContainer(children=[
        rhythmtree.RhythmTreeLeaf()
        ])

    assert format(a) == format(b)
    assert a != b


def test_RhythmTreeContainer___eq___03():

    a = rhythmtree.RhythmTreeContainer(children=[])
    b = rhythmtree.RhythmTreeContainer(preprolated_duration=2, children=[])
    c = rhythmtree.RhythmTreeContainer(preprolated_duration=1, children=[
        rhythmtree.RhythmTreeLeaf(preprolated_duration=1)
        ])
    d = rhythmtree.RhythmTreeContainer(preprolated_duration=2, children=[
        rhythmtree.RhythmTreeLeaf(preprolated_duration=1)
        ])
    e = rhythmtree.RhythmTreeContainer(preprolated_duration=2, children=[
        rhythmtree.RhythmTreeLeaf(preprolated_duration=2)
        ])

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
