# -*- coding: utf-8 -*-
from abjad.tools import rhythmtreetools


def test_rhythmtreetools_RhythmTreeContainer___eq___01():

    a = rhythmtreetools.RhythmTreeContainer(children=[])
    b = rhythmtreetools.RhythmTreeContainer(children=[])

    assert format(a) == format(b)
    assert a != b


def test_rhythmtreetools_RhythmTreeContainer___eq___02():

    a = rhythmtreetools.RhythmTreeContainer(children=[
        rhythmtreetools.RhythmTreeLeaf()
        ])
    b = rhythmtreetools.RhythmTreeContainer(children=[
        rhythmtreetools.RhythmTreeLeaf()
        ])

    assert format(a) == format(b)
    assert a != b


def test_rhythmtreetools_RhythmTreeContainer___eq___03():

    a = rhythmtreetools.RhythmTreeContainer(children=[])
    b = rhythmtreetools.RhythmTreeContainer(preprolated_duration=2, children=[])
    c = rhythmtreetools.RhythmTreeContainer(preprolated_duration=1, children=[
        rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
        ])
    d = rhythmtreetools.RhythmTreeContainer(preprolated_duration=2, children=[
        rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
        ])
    e = rhythmtreetools.RhythmTreeContainer(preprolated_duration=2, children=[
        rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
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
