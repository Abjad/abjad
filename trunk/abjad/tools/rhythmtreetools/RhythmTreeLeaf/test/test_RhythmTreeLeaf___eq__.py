from abjad.tools import rhythmtreetools


def test_RhythmTreeLeaf___eq___01():

    a = rhythmtreetools.RhythmTreeLeaf(1, True)
    b = rhythmtreetools.RhythmTreeLeaf(1, True)

    assert a == b


def test_RhythmTreeLeaf___eq___02():

    a = rhythmtreetools.RhythmTreeLeaf(1, True)
    b = rhythmtreetools.RhythmTreeLeaf(1, False)
    c = rhythmtreetools.RhythmTreeLeaf(2, True)
    d = rhythmtreetools.RhythmTreeLeaf(2, False)

    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
