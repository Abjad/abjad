# -*- encoding: utf-8 -*-
from abjad import *
from py.test import raises


def test_Note___init___01():
    r'''Init note with pitch in octave zero.
    '''

    note = Note(-37, (1, 4))
    assert note.lilypond_format == 'b,,,4'


def test_Note___init___02():
    r'''Init note with non-assignable duration.
    '''

    raises(AssignabilityError, 'Note(0, (5, 8))')


def test_Note___init___03():
    r'''Init note with LilyPond-style pitch string.
    '''

    note = Note('c,,', (1, 4))
    assert note.lilypond_format == 'c,,4'


def test_Note___init___04():
    r'''Init note with complete LilyPond-style note string.
    '''

    note = Note('cs8.')
    assert note.lilypond_format == 'cs8.'


def test_Note___init___05():
    r'''Init note with pitch, written duration and LilyPond multiplier.
    '''

    note = Note(12, (1, 4), (1, 2))
    assert isinstance(note, Note)


def test_Note___init___06():
    r'''Init note from chord.
    '''

    c = Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    n = Note(c)
    assert isinstance(n, Note)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(n) == dir(Note("c'4"))
    assert n._parent is None
    assert n.written_duration == duration


def test_Note___init___07():
    r'''Init note from tupletized chord.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = tuplet[0].written_duration
    note = Note(tuplet[0])
    assert isinstance(tuplet[0], Chord)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert isinstance(note, Note)


def test_Note___init___08():
    r'''Init note from beamed chord.
    '''

    staff = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    spannertools.BeamSpanner(staff[:])
    note = Note(staff[0])
    assert isinstance(staff[0], Chord)
    assert staff[0]._parent is staff
    assert isinstance(note, Note)


def test_Note___init___09():
    r'''Init note from rest.
    '''

    r = Rest((1, 8))
    d = r.written_duration
    n = Note(r)
    assert isinstance(n, Note)
    # check that attributes have not been removed or added.
    assert dir(r) == dir(Rest((1, 4)))
    assert dir(n) == dir(Note("c'4"))
    assert n._parent is None
    assert n.written_duration == d
    assert isinstance(r, Rest)


def test_Note___init___10():
    r'''Init note from tupletized rest.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Rest((1, 8)) * 3)
    d = tuplet[0].written_duration
    note = Note(tuplet[0])
    assert isinstance(tuplet[0], Rest)
    assert isinstance(note, Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert note._parent is None


def test_Note___init___11():
    r'''Init note from beamed rest.
    '''

    staff = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    spannertools.BeamSpanner(staff[:])
    note = Note(staff[1])
    assert isinstance(staff[1], Rest)
    assert isinstance(note, Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_Note___init___12():
    r'''Cast skip as note.
    '''
    skip = skiptools.Skip((1, 8))
    d = skip.written_duration
    n = Note(skip)
    assert isinstance(n, Note)
    assert dir(skip) == dir(skiptools.Skip((1, 4)))
    assert dir(n) == dir(Note("c'4"))
    assert n._parent is None
    assert n.written_duration == d


def test_Note___init___13():
    r'''Init note from tupletized skip.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), skiptools.Skip((1, 8)) * 3)
    d = tuplet[0].written_duration
    note = Note(tuplet[0])
    assert isinstance(tuplet[0], skiptools.Skip)
    assert isinstance(note, Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert note._parent is None


def test_Note___init___14():
    r'''Init note from beamed skip.
    '''

    staff = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
    spannertools.BeamSpanner(staff[:])
    note = Note(staff[1])
    assert isinstance(staff[1], skiptools.Skip)
    assert isinstance(note, Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_Note___init___15():
    r'''Init note with cautionary accidental.
    '''

    note = Note("c'?4")
    assert note.lilypond_format == "c'?4"


def test_Note___init___16():
    r'''Init note with forced accidental.
    '''

    note = Note("c'!4")
    assert note.lilypond_format == "c'!4"


def test_Note___init___17():
    r'''Init note with both forced and cautionary accidental.
    '''

    note = Note("c'!?4")
    assert note.lilypond_format == "c'!?4"


def test_Note___init___18():
    r'''Init note from chord with forced and cautionary accidental.
    '''

    c = Chord("<c'!? e' g'>4")
    note = Note(c)
    assert note.lilypond_format == "c'!?4"
