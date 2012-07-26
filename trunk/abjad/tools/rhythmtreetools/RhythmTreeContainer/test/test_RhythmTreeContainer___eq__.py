from abjad.tools import rhythmtreetools


def test_RhythmTreeContainer___eq___01():

    a = rhythmtreetools.RhythmTreeContainer(1, [])
    b = rhythmtreetools.RhythmTreeContainer(1, [])

    assert a == b


def test_RhythmTreeContainer___eq___02():

    a = rhythmtreetools.RhythmTreeContainer(1, [
        rhythmtreetools.RhythmTreeLeaf(1)
        ])
    b = rhythmtreetools.RhythmTreeContainer(1, [
        rhythmtreetools.RhythmTreeLeaf(1)
        ])

    assert a == b


def test_RhythmTreeContainer___eq___03():

    a = rhythmtreetools.RhythmTreeContainer(1, [])
    b = rhythmtreetools.RhythmTreeContainer(2, [])
    c = rhythmtreetools.RhythmTreeContainer(1, [
        rhythmtreetools.RhythmTreeLeaf(1)
        ])
    d = rhythmtreetools.RhythmTreeContainer(2, [
        rhythmtreetools.RhythmTreeLeaf(1)
        ])
    e = rhythmtreetools.RhythmTreeContainer(2, [
        rhythmtreetools.RhythmTreeLeaf(2)
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

