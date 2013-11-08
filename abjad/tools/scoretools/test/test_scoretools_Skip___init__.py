# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Skip___init___01():
    r'''Init skip from LilyPond input string.
    '''

    skip = scoretools.Skip('s8.')
    assert isinstance(skip, scoretools.Skip)


def test_scoretools_Skip___init___02():
    r'''Init skip from written duration and LilyPond multiplier.
    '''

    skip = scoretools.Skip((1, 4), (1, 2))

    assert isinstance(skip, scoretools.Skip)


def test_scoretools_Skip___init___03():
    r'''Init skip from containerize note.
    '''

    c = Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    skip = scoretools.Skip(c)
    assert isinstance(skip, scoretools.Skip)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(skip) == dir(scoretools.Skip((1, 4)))
    assert skip._parent is None
    assert skip.written_duration == duration


def test_scoretools_Skip___init___04():
    r'''Init skip from tupletized note.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = tuplet[0].written_duration
    skip = scoretools.Skip(tuplet[0])
    assert isinstance(tuplet[0], Chord)
    assert isinstance(skip, scoretools.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert skip._parent is None


def test_scoretools_Skip___init___05():
    r'''Init skip from beamed chord.
    '''

    staff = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    beam = Beam()
    attach(beam, staff[:])
    skip = scoretools.Skip(staff[0])
    assert isinstance(staff[0], Chord)
    assert isinstance(skip, scoretools.Skip)
    assert staff[0]._parent is staff
    assert skip._parent is None


def test_scoretools_Skip___init___06():
    note = Note(2, (1, 8))
    d = note.written_duration
    skip = scoretools.Skip(note)
    assert isinstance(skip, scoretools.Skip)
    # check that attributes have not been removed or added.
    assert dir(note) == dir(Note("c'4"))
    assert dir(skip) == dir(scoretools.Skip((1, 4)))
    assert format(skip) == 's8'
    assert skip._parent is None
    assert skip.written_duration == d


def test_scoretools_Skip___init___07():
    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    d = tuplet[0].written_duration
    skip = scoretools.Skip(tuplet[0])
    assert isinstance(tuplet[0], Note)
    assert isinstance(skip, scoretools.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d


def test_scoretools_Skip___init___08():
    r'''Init skip from beamed note.
    '''

    staff = Staff(Note(0, (1, 8)) * 3)
    beam = Beam()
    attach(beam, staff[:])
    skip = scoretools.Skip(staff[0])
    assert isinstance(staff[0], Note)
    assert isinstance(skip, scoretools.Skip)
    assert staff[0]._parent is staff


def test_scoretools_Skip___init___09():
    r'''Init skip from unincorporaed rest.
    '''

    rest = Rest((1, 8))
    d = rest.written_duration
    skip = scoretools.Skip(rest)
    assert isinstance(skip, scoretools.Skip)
    # check that attributes have not been removed or added.
    assert dir(rest) == dir(Rest((1, 4)))
    assert dir(skip) == dir(scoretools.Skip((1, 4)))
    assert skip._parent is None
    assert skip.written_duration == d


def test_scoretools_Skip___init___10():
    r'''Init skip from tupletized rest.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), Rest((1, 8)) * 3)
    d = tuplet[0].written_duration
    skip = scoretools.Skip(tuplet[0])
    assert isinstance(skip, scoretools.Skip)
    assert isinstance(tuplet[0], Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert skip._parent is None


def test_scoretools_Skip___init___11():
    r'''Init skip from spanned rest.
    '''

    staff = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    beam = Beam()
    attach(beam, staff[:])
    skip = scoretools.Skip(staff[1])
    assert isinstance(skip, scoretools.Skip)
    assert isinstance(staff[1], Rest)
    assert staff[1]._parent is staff
    assert skip._parent is None
