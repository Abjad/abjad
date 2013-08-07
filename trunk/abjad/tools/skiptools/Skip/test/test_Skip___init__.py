# -*- encoding: utf-8 -*-
from abjad import *


def test_Skip___init___01():
    r'''Init skip from LilyPond input string.
    '''

    skip = skiptools.Skip('s8.')
    assert isinstance(skip, skiptools.Skip)


def test_Skip___init___02():
    r'''Init skip from written duration and LilyPond multiplier.
    '''

    skip = skiptools.Skip((1, 4), (1, 2))

    assert isinstance(skip, skiptools.Skip)


def test_Skip___init___03():
    r'''Init skip from containerize note.
    '''

    c = Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    s = skiptools.Skip(c)
    assert isinstance(s, skiptools.Skip)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert s._parent is None
    assert s.written_duration == duration


def test_Skip___init___04():
    r'''Init skip from tupletized note.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = tuplet[0].written_duration
    skip = skiptools.Skip(tuplet[0])
    assert isinstance(tuplet[0], Chord)
    assert isinstance(skip, skiptools.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert skip._parent is None


def test_Skip___init___05():
    r'''Init skip from beamed chord.
    '''

    staff = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    spannertools.BeamSpanner(staff[:])
    skip = skiptools.Skip(staff[0])
    assert isinstance(staff[0], Chord)
    assert isinstance(skip, skiptools.Skip)
    assert staff[0]._parent is staff
    assert skip._parent is None


def test_Skip___init___06():
    n = Note(2, (1, 8))
    d = n.written_duration
    s = skiptools.Skip(n)
    assert isinstance(s, skiptools.Skip)
    # check that attributes have not been removed or added.
    assert dir(n) == dir(Note("c'4"))
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert s.lilypond_format == 's8'
    assert s._parent is None
    assert s.written_duration == d


def test_Skip___init___07():
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    d = tuplet[0].written_duration
    skip = skiptools.Skip(tuplet[0])
    assert isinstance(tuplet[0], Note)
    assert isinstance(skip, skiptools.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d


def test_Skip___init___08():
    r'''Init skip from beamed note.
    '''

    staff = Staff(Note(0, (1, 8)) * 3)
    spannertools.BeamSpanner(staff[:])
    skip = skiptools.Skip(staff[0])
    assert isinstance(staff[0], Note)
    assert isinstance(skip, skiptools.Skip)
    assert staff[0]._parent is staff


def test_Skip___init___09():
    r'''Init skip from unincorporaed rest.
    '''

    r = Rest((1, 8))
    d = r.written_duration
    s = skiptools.Skip(r)
    assert isinstance(s, skiptools.Skip)
    # check that attributes have not been removed or added.
    assert dir(r) == dir(Rest((1, 4)))
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert s._parent is None
    assert s.written_duration == d


def test_Skip___init___10():
    r'''Init skip from tupletized rest.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Rest((1, 8)) * 3)
    d = tuplet[0].written_duration
    skip = skiptools.Skip(tuplet[0])
    assert isinstance(skip, skiptools.Skip)
    assert isinstance(tuplet[0], Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert skip._parent is None


def test_Skip___init___11():
    r'''Init skip from spanned rest.
    '''

    staff = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    spannertools.BeamSpanner(staff[:])
    skip = skiptools.Skip(staff[1])
    assert isinstance(skip, skiptools.Skip)
    assert isinstance(staff[1], Rest)
    assert staff[1]._parent is staff
    assert skip._parent is None
