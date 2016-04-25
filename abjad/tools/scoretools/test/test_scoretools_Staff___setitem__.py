# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Staff___setitem___01():
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
    staff[1] = Chord([12, 13, 15], (1, 4))
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    assert isinstance(staff[0], Note)
    assert isinstance(staff[1], Chord)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], scoretools.Skip)
    assert isinstance(staff[4], scoretools.FixedDurationTuplet)
    staff[0] = Rest((1, 4))
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    assert isinstance(staff[0], Rest)
    assert isinstance(staff[1], Chord)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], scoretools.Skip)
    assert isinstance(staff[4], scoretools.FixedDurationTuplet)
    staff[-2] = scoretools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    assert isinstance(staff[0], Rest)
    assert isinstance(staff[1], Chord)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], scoretools.FixedDurationTuplet)
    assert isinstance(staff[4], scoretools.FixedDurationTuplet)
    staff[-1] = Note(13, (1, 4))
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    assert isinstance(staff[0], Rest)
    assert isinstance(staff[1], Chord)
    assert isinstance(staff[2], Chord)
    assert isinstance(staff[3], scoretools.FixedDurationTuplet)
    assert isinstance(staff[4], Note)
    staff[-3] = scoretools.Skip((1, 4))
    assert len(staff) == 5
    assert inspect_(staff).is_well_formed()
    assert isinstance(staff[0], Rest)
    assert isinstance(staff[1], Chord)
    assert isinstance(staff[2], scoretools.Skip)
    assert isinstance(staff[3], scoretools.FixedDurationTuplet)
    assert isinstance(staff[4], Note)


def test_scoretools_Staff___setitem___02():
    r'''Reassign the *entire* contents of staff.
    '''
    staff = Staff(Note("c'4") * 4)
    assert staff._contents_duration == Duration(4, 4)
    staff[:] = Note(0, (1, 8)) * 4
    assert staff._contents_duration == Duration(4, 8)


def test_scoretools_Staff___setitem___03():
    r'''Item-assign an empty container to staff.
    '''
    staff = Staff(Note("c'4") * 4)
    staff[0] = Voice([])


def test_scoretools_Staff___setitem___04():
    r'''Slice-assign empty containers to staff.
    '''
    staff = Staff(Note("c'4") * 4)
    staff[0:2] = [Voice([]), Voice([])]


def test_scoretools_Staff___setitem___05():
    r'''Bark when user assigns a slice to an item.
    '''

    staff = Staff(Note("c'4") * 4)

    statement = 'staff[0] = [Note(2, (1, 4)), Note(2, (1, 4))]'
    assert pytest.raises(AssertionError, statement)


def test_scoretools_Staff___setitem___06():
    r'''Bark when user assigns an item to a slice.
    '''

    staff = Staff(Note("c'4") * 4)

    assert pytest.raises(Exception, 'staff[0:2] = Note(2, (1, 4))')


def test_scoretools_Staff___setitem___07():
    r'''Slice-assign notes.
    '''

    staff = Staff(Note(0, (1, 8)) * 8)
    staff[0:4] = Note(2, (1, 8)) * 4
    assert len(staff) == 8
    for x in staff[0:4]:
        assert x.written_pitch.numbered_pitch._pitch_number == 2
    for x in staff[4:8]:
        assert x.written_pitch.numbered_pitch._pitch_number == 0
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___setitem___08():
    r'''Slice-assign chords.
    '''

    staff = Staff(Note(0, (1, 8)) * 8)
    staff[0:4] = Chord([2, 3, 4], (1, 4)) * 4
    assert len(staff) == 8
    for x in staff[0:4]:
        assert x.written_duration == Duration(1, 4)
    for x in staff[4:8]:
        assert x.written_duration == Duration(1, 8)
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___setitem___09():
    r'''Slice-assign tuplets.
    '''

    staff = Staff(Note(0, (1, 8)) * 8)
    staff[0:4] = scoretools.FixedDurationTuplet(
        Duration(2, 8), Note(0, (1, 8)) * 3) * 2
    assert len(staff) == 6
    for i, x in enumerate(staff):
        if i in [0, 1]:
            assert isinstance(x, scoretools.FixedDurationTuplet)
        else:
            assert isinstance(x, Note)
    assert inspect_(staff).is_well_formed()


def test_scoretools_Staff___setitem___10():
    r'''Slice-assign measures.
    '''

    staff = Staff(Note(0, (1, 8)) * 8)
    staff[0:4] = Measure((2, 8), Note(0, (1, 8)) * 2) * 2
    assert len(staff) == 6
    for i, x in enumerate(staff):
        if i in [0, 1]:
            assert isinstance(x, Measure)
        else:
            assert isinstance(x, Note)
    assert inspect_(staff).is_well_formed()
