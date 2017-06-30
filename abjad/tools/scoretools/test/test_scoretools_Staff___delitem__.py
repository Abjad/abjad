# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Staff___delitem___01():

    staff = Staff([
        Note("c'4"),
        Rest((1, 4)),
        Chord([2, 3, 4], (1, 4)),
        Skip((1, 4)),
        Tuplet((4, 5), 4 * Note(0, (1, 16))),
        ])

    assert len(staff) == 5
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], Skip)
    assert isinstance(staff[4], Tuplet)
    del(staff[0])
    assert len(staff) == 4
    assert isinstance(staff[0], Rest)
    assert isinstance(staff[1], Chord)
    assert isinstance(staff[2], Skip)
    assert isinstance(staff[3], Tuplet)
    del(staff[0])
    assert len(staff) == 3
    assert isinstance(staff[0], Chord)
    assert isinstance(staff[1], Skip)
    assert isinstance(staff[2], Tuplet)
    del(staff[0])
    assert len(staff) == 2
    assert isinstance(staff[0], Skip)
    assert isinstance(staff[1], Tuplet)
    del(staff[0])
    assert len(staff) == 1
    assert isinstance(staff[0], Tuplet)
    del(staff[0])
    assert len(staff) == 0


def test_scoretools_Staff___delitem___02():

    staff = Staff([
        Note("c'4"),
        Rest((1, 4)),
        Chord([2, 3, 4], (1, 4)),
        Skip((1, 4)),
        Tuplet((4, 5), 4 * Note(0, (1, 16))),
        ])

    assert len(staff) == 5
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], Skip)
    assert isinstance(staff[4], Tuplet)
    del(staff[-1])
    assert len(staff) == 4
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], Skip)
    del(staff[-1])
    assert len(staff) == 3
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Chord)
    del(staff[-1])
    assert len(staff) == 2
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    del(staff[-1])
    assert len(staff) == 1
    assert isinstance(staff[0], Note)
    del(staff[-1])
    assert len(staff) == 0


def test_scoretools_Staff___delitem___03():

    staff = Staff([
        Note("c'4"),
        Rest((1, 4)),
        Chord([2, 3, 4], (1, 4)),
        Skip((1, 4)),
        Tuplet((4, 5), 4 * Note(0, (1, 16))),
        ])

    assert len(staff) == 5
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], Skip)
    assert isinstance(staff[4], Tuplet)
    del(staff[3])
    assert len(staff) == 4
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], Tuplet)
    del(staff[-2])
    assert len(staff) == 3
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Tuplet)
    del(staff[2])
    assert len(staff) == 2
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    del(staff[0])
    assert len(staff) == 1
    assert isinstance(staff[0], Rest)
    del(staff[-1])
    assert len(staff) == 0
