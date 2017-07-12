# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Note___init___01():
    r'''Initializes note from empty input.
    '''

    note = abjad.Note()

    assert format(note) == "c'4"


def test_scoretools_Note___init___02():
    r'''Initializes note with pitch in octave zero.
    '''

    note = abjad.Note(-37, (1, 4))

    assert format(note) == 'b,,,4'


def test_scoretools_Note___init___03():
    r'''Initializes note with non-assignable duration.
    '''

    pytest.raises(AssignabilityError, 'abjad.Note(0, (5, 8))')


def test_scoretools_Note___init___04():
    r'''Initializes note with LilyPond-style pitch string.
    '''

    note = abjad.Note('c,,', (1, 4))

    assert format(note) == 'c,,4'


def test_scoretools_Note___init___05():
    r'''Initializes note with complete LilyPond-style note string.
    '''

    note = abjad.Note('cs8.')

    assert format(note) == 'cs8.'


def test_scoretools_Note___init___06():
    r'''Initializes note from chord.
    '''

    chord = abjad.Chord([2, 3, 4], (1, 4))
    note = abjad.Note(chord)

    assert format(note) == abjad.String.normalize(
        r'''
        d'4
        '''
        )

    assert abjad.inspect(note).is_well_formed()


def test_scoretools_Note___init___07():
    r'''Initializes note from tupletized chord.
    '''

    chord = abjad.Chord([2, 3, 4], (1, 4))
    tuplet = abjad.Tuplet((2, 3), 3 * chord)
    note = abjad.Note(tuplet[0])

    assert format(note) == abjad.String.normalize(
        r'''
        d'4
        '''
        )

    assert abjad.inspect(note).is_well_formed()


def test_scoretools_Note___init___08():
    r'''Initializes note from beamed chord.
    '''

    chord = abjad.Chord([2, 3, 4], (1, 4))
    staff = abjad.Staff(3 * chord)
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    note = abjad.Note(staff[0])

    assert format(note) == abjad.String.normalize(
        r'''
        d'4
        '''
        )

    assert abjad.inspect(note).is_well_formed()


def test_scoretools_Note___init___09():
    r'''Initializes note from rest.
    '''

    rest = abjad.Rest('r8')
    note = abjad.Note(rest)

    assert format(note) == abjad.String.normalize(
        r'''
        8
        '''
        )

    assert abjad.inspect(note).is_well_formed()


def test_scoretools_Note___init___10():
    r'''Initializes note from tupletized rest.
    '''

    tuplet = abjad.Tuplet((2, 3), 3 * abjad.Rest((1, 8)))
    d = tuplet[0].written_duration
    note = abjad.Note(tuplet[0])

    assert isinstance(tuplet[0], abjad.Rest)
    assert isinstance(note, abjad.Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert note._parent is None


def test_scoretools_Note___init___11():
    r'''Initializes note from beamed rest.
    '''

    staff = abjad.Staff([abjad.Note(0, (1, 8)), abjad.Rest((1, 8)), abjad.Note(0, (1, 8))])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    note = abjad.Note(staff[1])

    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(note, abjad.Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_scoretools_Note___init___12():
    r'''Initializes notes from skip.
    '''

    skip = abjad.Skip((1, 8))
    d = skip.written_duration
    note = abjad.Note(skip)

    assert isinstance(note, abjad.Note)
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert dir(note) == dir(abjad.Note("c'4"))
    assert note._parent is None
    assert note.written_duration == d


def test_scoretools_Note___init___13():
    r'''Initializes note from tupletized skip.
    '''

    tuplet = abjad.Tuplet((2, 3), 3 * abjad.Skip((1, 8)))
    d = tuplet[0].written_duration
    note = abjad.Note(tuplet[0])

    assert isinstance(tuplet[0], abjad.Skip)
    assert isinstance(note, abjad.Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert note._parent is None


def test_scoretools_Note___init___14():
    r'''Initializes note from beamed skip.
    '''

    staff = abjad.Staff([abjad.Note(0, (1, 8)), abjad.Skip((1, 8)), abjad.Note(0, (1, 8))])
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])
    note = abjad.Note(staff[1])

    assert isinstance(staff[1], abjad.Skip)
    assert isinstance(note, abjad.Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_scoretools_Note___init___15():
    r'''Initializes note with cautionary accidental.
    '''

    note = abjad.Note("c'?4")

    assert format(note) == "c'?4"


def test_scoretools_Note___init___16():
    r'''Initializes note with forced accidental.
    '''

    note = abjad.Note("c'!4")

    assert format(note) == "c'!4"


def test_scoretools_Note___init___17():
    r'''Initializes note with both forced and cautionary accidental.
    '''

    note = abjad.Note("c'!?4")

    assert format(note) == "c'!?4"


def test_scoretools_Note___init___18():
    r'''Initializes note from chord with forced and cautionary accidental.
    '''

    chord = abjad.Chord("<c'!? e' g'>4")
    note = abjad.Note(chord)

    assert format(note) == "c'!?4"


def test_scoretools_Note___init___19():
    r'''Initialize note with drum pitch.
    '''

    note = abjad.Note('sn4')

    assert format(note) == 'snare4'
