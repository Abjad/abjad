import abjad
import abjad.rhythmtrees


def test_RhythmTreeLeaf___eq___01():

    a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)
    b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)

    assert abjad.storage(a) == abjad.storage(b)
    assert a != b


def test_RhythmTreeLeaf___eq___02():

    a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)
    b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1, is_pitched=False)
    c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2, is_pitched=True)
    d = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2, is_pitched=False)

    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
