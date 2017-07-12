# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Skip___init___01():
    r'''Initialize skip from LilyPond input string.
    '''

    skip = abjad.Skip('s8.')
    assert isinstance(skip, abjad.Skip)


def test_scoretools_Skip___init___02():
    r'''Initialize skip from containerize note.
    '''

    c = abjad.Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    skip = abjad.Skip(c)
    assert isinstance(skip, abjad.Skip)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(abjad.Chord([2, 3, 4], (1, 4)))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert skip._parent is None
    assert skip.written_duration == duration


def test_scoretools_Skip___init___03():
    r'''Initialize skip from tupletized note.
    '''

    tuplet = abjad.Tuplet((2, 3), 3 * abjad.Chord([2, 3, 4], (1, 4)))
    d = tuplet[0].written_duration
    skip = abjad.Skip(tuplet[0])
    assert isinstance(tuplet[0], abjad.Chord)
    assert isinstance(skip, abjad.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert skip._parent is None


def test_scoretools_Skip___init___04():
    r'''Initialize skip from beamed chord.
    '''

    staff = abjad.Staff(abjad.Chord([2, 3, 4], (1, 4)) * 3)
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    skip = abjad.Skip(staff[0])
    assert isinstance(staff[0], abjad.Chord)
    assert isinstance(skip, abjad.Skip)
    assert staff[0]._parent is staff
    assert skip._parent is None


def test_scoretools_Skip___init___05():

    note = abjad.Note(2, (1, 8))
    d = note.written_duration
    skip = abjad.Skip(note)
    assert isinstance(skip, abjad.Skip)
    # check that attributes have not been removed or added.
    assert dir(note) == dir(abjad.Note("c'4"))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert format(skip) == 's8'
    assert skip._parent is None
    assert skip.written_duration == d


def test_scoretools_Skip___init___06():

    tuplet = abjad.Tuplet((2, 3), 3 * abjad.Note(0, (1, 8)))
    d = tuplet[0].written_duration
    skip = abjad.Skip(tuplet[0])
    assert isinstance(tuplet[0], abjad.Note)
    assert isinstance(skip, abjad.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d


def test_scoretools_Skip___init___07():
    r'''Initialize skip from beamed note.
    '''

    staff = abjad.Staff(abjad.Note(0, (1, 8)) * 3)
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    skip = abjad.Skip(staff[0])
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(skip, abjad.Skip)
    assert staff[0]._parent is staff


def test_scoretools_Skip___init___08():
    r'''Initialize skip from unincorporaed rest.
    '''

    rest = abjad.Rest((1, 8))
    d = rest.written_duration
    skip = abjad.Skip(rest)
    assert isinstance(skip, abjad.Skip)
    # check that attributes have not been removed or added.
    assert dir(rest) == dir(abjad.Rest((1, 4)))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert skip._parent is None
    assert skip.written_duration == d


def test_scoretools_Skip___init___09():
    r'''Initialize skip from tupletized rest.
    '''

    tuplet = abjad.Tuplet((2, 3), 3 * abjad.Rest((1, 8)))
    d = tuplet[0].written_duration
    skip = abjad.Skip(tuplet[0])
    assert isinstance(skip, abjad.Skip)
    assert isinstance(tuplet[0], abjad.Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert skip._parent is None


def test_scoretools_Skip___init___10():
    r'''Initialize skip from spanned rest.
    '''

    staff = abjad.Staff([abjad.Note(0, (1, 8)), abjad.Rest((1, 8)), abjad.Note(0, (1, 8))])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    skip = abjad.Skip(staff[1])
    assert isinstance(skip, abjad.Skip)
    assert isinstance(staff[1], abjad.Rest)
    assert staff[1]._parent is staff
    assert skip._parent is None
