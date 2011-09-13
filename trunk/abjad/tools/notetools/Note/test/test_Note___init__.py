from abjad import *
from py.test import raises


def test_Note___init___01():
    '''Init note with pitch in octave zero.
    '''

    t = Note(-37, (1, 4))
    assert t.format == 'b,,,4'


def test_Note___init___02():
    '''Init note with non-assignable duration.
    '''

    raises(AssignabilityError, 'Note(0, (5, 8))')


def test_Note___init___03():
    '''Init note with LilyPond-style pitch string.
    '''

    t = Note('c,,', (1, 4))
    assert t.format == 'c,,4'


def test_Note___init___04():
    '''Init note with complete LilyPond-style note string.
    '''

    t = Note('cs8.')
    assert t.format == 'cs8.'


def test_Note___init___05():
    '''Init note with pitch, written duration and LilyPond multiplier.
    '''

    note = Note(12, (1, 4), (1, 2))
    assert isinstance(note, Note)


def test_Note___init___06():
    '''Init note from chord.
    '''

    c = Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    n = Note(c)
    assert isinstance(n, Note)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(n) == dir(Note("c'4"))
    assert n._parentage.parent is None
    assert n.written_duration == duration


def test_Note___init___07():
    '''Init note from tupletized chord.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = t[0].written_duration
    note = Note(t[0])
    assert isinstance(t[0], Chord)
    assert t[0]._parentage.parent is t
    assert t[0].written_duration == d
    assert isinstance(note, Note)


def test_Note___init___08():
    '''Init note from beamed chord.
    '''

    t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    spannertools.BeamSpanner(t[:])
    note = Note(t[0])
    assert isinstance(t[0], Chord)
    assert t[0]._parentage.parent is t
    assert isinstance(note, Note)


def test_Note___init___09():
    '''Init note from rest.
    '''

    r = Rest((1, 8))
    d = r.written_duration
    n = Note(r)
    assert isinstance(n, Note)
    # check that attributes have not been removed or added.
    assert dir(r) == dir(Rest((1, 4)))
    assert dir(n) == dir(Note("c'4"))
    assert n._parentage.parent is None
    assert n.written_duration == d
    assert isinstance(r, Rest)


def test_Note___init___10():
    '''Init note from tupletized rest.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Rest((1, 8)) * 3)
    d = t[0].written_duration
    note = Note(t[0])
    assert isinstance(t[0], Rest)
    assert isinstance(note, Note)
    assert t[0]._parentage.parent is t
    assert t[0].written_duration == d
    assert note._parentage.parent is None


def test_Note___init___11():
    '''Init note from beamed rest.
    '''

    t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    spannertools.BeamSpanner(t[:])
    note = Note(t[1])
    assert isinstance(t[1], Rest)
    assert isinstance(note, Note)
    assert t[1]._parentage.parent is t
    assert note._parentage.parent is None


def test_Note___init___12():
    '''Cast skip as note.'''
    s = skiptools.Skip((1, 8))
    d = s.written_duration
    n = Note(s)
    assert isinstance(n, Note)
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert dir(n) == dir(Note("c'4"))
    assert n._parentage.parent is None
    assert n.written_duration == d


def test_Note___init___13():
    '''Init note from tupletized skip.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), skiptools.Skip((1, 8)) * 3)
    d = t[0].written_duration
    note = Note(t[0])
    assert isinstance(t[0], skiptools.Skip)
    assert isinstance(note, Note)
    assert t[0]._parentage.parent is t
    assert t[0].written_duration == d
    assert note._parentage.parent is None


def test_Note___init___14():
    '''Init note from beamed skip.
    '''

    t = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
    spannertools.BeamSpanner(t[:])
    note = Note(t[1])
    assert isinstance(t[1], skiptools.Skip)
    assert isinstance(note, Note)
    assert t[1]._parentage.parent is t
    assert note._parentage.parent is None
