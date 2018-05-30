import abjad
from abjad import rhythmtree


def test_RhythmTreeLeaf___eq___01():

    a = rhythmtree.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)
    b = rhythmtree.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)

    assert format(a) == format(b)
    assert a != b


def test_RhythmTreeLeaf___eq___02():

    a = rhythmtree.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)
    b = rhythmtree.RhythmTreeLeaf(preprolated_duration=1, is_pitched=False)
    c = rhythmtree.RhythmTreeLeaf(preprolated_duration=2, is_pitched=True)
    d = rhythmtree.RhythmTreeLeaf(preprolated_duration=2, is_pitched=False)

    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
