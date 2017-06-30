# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Staff_append_01():
    r'''Append one note.
    '''

    staff = Staff(Note("c'4") * 4)
    staff.append(Note("c'4"))
    assert inspect_(staff).is_well_formed()
    assert len(staff) == 5
    assert staff._get_contents_duration() == Duration(5, 4)


def test_scoretools_Staff_append_02():
    r'''Append one chord.
    '''

    staff = Staff(Note("c'4") * 4)
    staff.append(Chord([2, 3, 4], (1, 4)))
    assert inspect_(staff).is_well_formed()
    assert len(staff) == 5
    assert staff._get_contents_duration() == Duration(5, 4)


def test_scoretools_Staff_append_03():
    r'''Append one tuplet.
    '''

    staff = Staff(Note("c'4") * 4)
    staff.append(Tuplet((2, 3), 3 * Note(0, (1, 8))))
    assert inspect_(staff).is_well_formed()
    assert len(staff) == 5
    assert staff._get_contents_duration() == Duration(5, 4)
