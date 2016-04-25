# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Staff_append_01():
    r'''Append one note.
    '''

    staff = Staff(Note("c'4") * 4)
    staff.append(Note("c'4"))
    assert inspect_(staff).is_well_formed()
    assert len(staff) == 5
    assert staff._contents_duration == Duration(5, 4)


def test_scoretools_Staff_append_02():
    r'''Append one chord.
    '''

    staff = Staff(Note("c'4") * 4)
    staff.append(Chord([2, 3, 4], (1, 4)))
    assert inspect_(staff).is_well_formed()
    assert len(staff) == 5
    assert staff._contents_duration == Duration(5, 4)


def test_scoretools_Staff_append_03():
    r'''Append one tuplet.
    '''

    staff = Staff(Note("c'4") * 4)
    staff.append(scoretools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3))
    assert inspect_(staff).is_well_formed()
    assert len(staff) == 5
    assert staff._contents_duration == Duration(5, 4)


def test_scoretools_Staff_append_04():
    r'''Empty containers are allowed but not well-formed.
    '''

    staff = Staff(Note("c'4") * 4)
    staff.append(scoretools.FixedDurationTuplet(Duration(2, 8), []))
    assert len(staff) == 5
    assert staff._contents_duration == Duration(5, 4)
