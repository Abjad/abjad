# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Staff___getitem___01():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Rest)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], scoretools.Skip)
    assert isinstance(staff[4], scoretools.FixedDurationTuplet)
    assert isinstance(staff[-5], Note)
    assert isinstance(staff[-4], Rest)
    assert isinstance(staff[-3], Chord)
    assert isinstance(staff[-2], scoretools.Skip)
    assert isinstance(staff[-1], scoretools.FixedDurationTuplet)


def test_scoretools_Staff___getitem___02():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    slice = staff[0:0]
    assert len(slice) == 0
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___getitem___03():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    slice = staff[0:1]
    assert len(slice) == 1
    assert isinstance(slice[0], Note)
    for x in staff:
        assert x._parent == staff
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___getitem___04():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    slice = staff[-1:]
    assert len(slice) == 1
    assert isinstance(slice[0], scoretools.FixedDurationTuplet)
    for x in slice:
        assert x._parent == staff
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___getitem___05():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    slice = staff[1:-1]
    assert len(slice) == 3
    assert isinstance(slice[0], Rest)
    assert isinstance(slice[1], Chord)
    assert isinstance(slice[2], scoretools.Skip)
    for x in slice:
        assert x._parent == staff
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___getitem___06():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    slice = staff[2:]
    assert len(slice) == 3
    assert isinstance(slice[0], Chord)
    assert isinstance(slice[1], scoretools.Skip)
    assert isinstance(slice[2], scoretools.FixedDurationTuplet)
    for x in slice:
        assert x._parent == staff
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___getitem___07():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    slice = staff[:-2]
    assert len(slice) == 3
    assert isinstance(slice[0], Note)
    assert isinstance(slice[1], Rest)
    assert isinstance(slice[2], Chord)
    for x in slice:
        assert x._parent == staff
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___getitem___08():
    staff = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            scoretools.Skip((1, 4)),
            scoretools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    slice = staff[:]
    assert len(slice) == 5
    assert isinstance(slice, (list, selectiontools.Selection))
    assert isinstance(slice[0], Note)
    assert isinstance(slice[1], Rest)
    assert isinstance(slice[2], Chord)
    assert isinstance(slice[3], scoretools.Skip)
    assert isinstance(slice[4], scoretools.FixedDurationTuplet)
    for x in slice:
        assert x._parent == staff
    assert inspect_(staff).is_well_formed()
