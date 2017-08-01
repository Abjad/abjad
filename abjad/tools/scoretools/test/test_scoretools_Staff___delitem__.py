# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Staff___delitem___01():

    staff = abjad.Staff([
        abjad.Note("c'4"),
        abjad.Rest((1, 4)),
        abjad.Chord([2, 3, 4], (1, 4)),
        abjad.Skip((1, 4)),
        abjad.Tuplet((4, 5), 4 * abjad.Note(0, (1, 16))),
        ])

    assert len(staff) == 5
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    del(staff[0])
    assert len(staff) == 4
    assert isinstance(staff[0], abjad.Rest)
    assert isinstance(staff[1], abjad.Chord)
    assert isinstance(staff[2], abjad.Skip)
    assert isinstance(staff[3], abjad.Tuplet)
    del(staff[0])
    assert len(staff) == 3
    assert isinstance(staff[0], abjad.Chord)
    assert isinstance(staff[1], abjad.Skip)
    assert isinstance(staff[2], abjad.Tuplet)
    del(staff[0])
    assert len(staff) == 2
    assert isinstance(staff[0], abjad.Skip)
    assert isinstance(staff[1], abjad.Tuplet)
    del(staff[0])
    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Tuplet)
    del(staff[0])
    assert len(staff) == 0


def test_scoretools_Staff___delitem___02():

    staff = abjad.Staff([
        abjad.Note("c'4"),
        abjad.Rest((1, 4)),
        abjad.Chord([2, 3, 4], (1, 4)),
        abjad.Skip((1, 4)),
        abjad.Tuplet((4, 5), 4 * abjad.Note(0, (1, 16))),
        ])

    assert len(staff) == 5
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    del(staff[-1])
    assert len(staff) == 4
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    del(staff[-1])
    assert len(staff) == 3
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    del(staff[-1])
    assert len(staff) == 2
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    del(staff[-1])
    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Note)
    del(staff[-1])
    assert len(staff) == 0


def test_scoretools_Staff___delitem___03():

    staff = abjad.Staff([
        abjad.Note("c'4"),
        abjad.Rest((1, 4)),
        abjad.Chord([2, 3, 4], (1, 4)),
        abjad.Skip((1, 4)),
        abjad.Tuplet((4, 5), 4 * abjad.Note(0, (1, 16))),
        ])

    assert len(staff) == 5
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    del(staff[3])
    assert len(staff) == 4
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Tuplet)
    del(staff[-2])
    assert len(staff) == 3
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Tuplet)
    del(staff[2])
    assert len(staff) == 2
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    del(staff[0])
    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Rest)
    del(staff[-1])
    assert len(staff) == 0
