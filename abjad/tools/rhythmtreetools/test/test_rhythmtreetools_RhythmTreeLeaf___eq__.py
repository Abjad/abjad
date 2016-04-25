# -*- coding: utf-8 -*-
from abjad.tools import rhythmtreetools


def test_rhythmtreetools_RhythmTreeLeaf___eq___01():

    a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)
    b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)

    assert format(a) == format(b)
    assert a != b


def test_rhythmtreetools_RhythmTreeLeaf___eq___02():

    a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1, is_pitched=True)
    b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1, is_pitched=False)
    c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2, is_pitched=True)
    d = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2, is_pitched=False)

    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
