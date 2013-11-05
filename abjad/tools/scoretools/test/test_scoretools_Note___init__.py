# -*- encoding: utf-8 -*-
from abjad import *
from pytest import raises


def test_scoretools_Note___init___01():
    r'''Init note with pitch in octave zero.
    '''

    note = Note(-37, (1, 4))
    assert format(note) == 'b,,,4'


def test_scoretools_Note___init___02():
    r'''Init note with non-assignable duration.
    '''

    raises(AssignabilityError, 'Note(0, (5, 8))')


def test_scoretools_Note___init___03():
    r'''Init note with LilyPond-style pitch string.
    '''

    note = Note('c,,', (1, 4))
    assert format(note) == 'c,,4'


def test_scoretools_Note___init___04():
    r'''Init note with complete LilyPond-style note string.
    '''

    note = Note('cs8.')
    assert format(note) == 'cs8.'


def test_scoretools_Note___init___05():
    r'''Init note with pitch, written duration and LilyPond multiplier.
    '''

    note = Note(12, (1, 4), (1, 2))
    assert isinstance(note, Note)


def test_scoretools_Note___init___06():
    r'''Init note from chord.
    '''

    c = Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    note = Note(c)
    assert isinstance(note, Note)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(note) == dir(Note("c'4"))
    assert note._parent is None
    assert note.written_duration == duration


def test_scoretools_Note___init___07():
    r'''Init note from tupletized chord.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = tuplet[0].written_duration
    note = Note(tuplet[0])
    assert isinstance(tuplet[0], Chord)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert isinstance(note, Note)


def test_scoretools_Note___init___08():
    r'''Init note from beamed chord.
    '''

    staff = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:])
    note = Note(staff[0])
    assert isinstance(staff[0], Chord)
    assert staff[0]._parent is staff
    assert isinstance(note, Note)


def test_scoretools_Note___init___09():
    r'''Init note from rest.
    '''

    rest = Rest((1, 8))
    d = rest.written_duration
    note = Note(rest)
    assert isinstance(note, Note)
    # check that attributes have not been removed or added.
    assert dir(rest) == dir(Rest((1, 4)))
    assert dir(note) == dir(Note("c'4"))
    assert note._parent is None
    assert note.written_duration == d
    assert isinstance(rest, Rest)


def test_scoretools_Note___init___10():
    r'''Init note from tupletized rest.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), Rest((1, 8)) * 3)
    d = tuplet[0].written_duration
    note = Note(tuplet[0])
    assert isinstance(tuplet[0], Rest)
    assert isinstance(note, Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert note._parent is None


def test_scoretools_Note___init___11():
    r'''Init note from beamed rest.
    '''

    staff = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:])
    note = Note(staff[1])
    assert isinstance(staff[1], Rest)
    assert isinstance(note, Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_scoretools_Note___init___12():
    r'''Cast skip as note.
    '''
    skip = scoretools.Skip((1, 8))
    d = skip.written_duration
    note = Note(skip)
    assert isinstance(note, Note)
    assert dir(skip) == dir(scoretools.Skip((1, 4)))
    assert dir(note) == dir(Note("c'4"))
    assert note._parent is None
    assert note.written_duration == d


def test_scoretools_Note___init___13():
    r'''Init note from tupletized skip.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), scoretools.Skip((1, 8)) * 3)
    d = tuplet[0].written_duration
    note = Note(tuplet[0])
    assert isinstance(tuplet[0], scoretools.Skip)
    assert isinstance(note, Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert note._parent is None


def test_scoretools_Note___init___14():
    r'''Init note from beamed skip.
    '''

    staff = Staff([Note(0, (1, 8)), scoretools.Skip((1, 8)), Note(0, (1, 8))])
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:])
    note = Note(staff[1])
    assert isinstance(staff[1], scoretools.Skip)
    assert isinstance(note, Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_scoretools_Note___init___15():
    r'''Init note with cautionary accidental.
    '''

    note = Note("c'?4")
    assert format(note) == "c'?4"


def test_scoretools_Note___init___16():
    r'''Init note with forced accidental.
    '''

    note = Note("c'!4")
    assert format(note) == "c'!4"


def test_scoretools_Note___init___17():
    r'''Init note with both forced and cautionary accidental.
    '''

    note = Note("c'!?4")
    assert format(note) == "c'!?4"


def test_scoretools_Note___init___18():
    r'''Init note from chord with forced and cautionary accidental.
    '''

    c = Chord("<c'!? e' g'>4")
    note = Note(c)
    assert format(note) == "c'!?4"
