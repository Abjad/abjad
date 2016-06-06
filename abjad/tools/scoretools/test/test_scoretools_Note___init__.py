# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Note___init___01():
    r'''Initializes note from empty input.
    '''

    note = Note()

    assert format(note) == "c'4"


def test_scoretools_Note___init___02():
    r'''Initializes note with pitch in octave zero.
    '''

    note = Note(-37, (1, 4))

    assert format(note) == 'b,,,4'


def test_scoretools_Note___init___03():
    r'''Initializes note with non-assignable duration.
    '''

    pytest.raises(AssignabilityError, 'Note(0, (5, 8))')


def test_scoretools_Note___init___04():
    r'''Initializes note with LilyPond-style pitch string.
    '''

    note = Note('c,,', (1, 4))

    assert format(note) == 'c,,4'


def test_scoretools_Note___init___05():
    r'''Initializes note with complete LilyPond-style note string.
    '''

    note = Note('cs8.')

    assert format(note) == 'cs8.'


def test_scoretools_Note___init___06():
    r'''Initializes note from chord.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    note = Note(chord)

    assert format(note) == stringtools.normalize(
        r'''
        d'4
        '''
        )

    assert inspect_(note).is_well_formed()


def test_scoretools_Note___init___07():
    r'''Initializes note from tupletized chord.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    tuplet = Tuplet((2, 3), 3 * chord)
    note = Note(tuplet[0])

    assert format(note) == stringtools.normalize(
        r'''
        d'4
        '''
        )

    assert inspect_(note).is_well_formed()


def test_scoretools_Note___init___08():
    r'''Initializes note from beamed chord.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    staff = Staff(3 * chord)
    beam = Beam()
    attach(beam, staff[:])
    note = Note(staff[0])

    assert format(note) == stringtools.normalize(
        r'''
        d'4
        '''
        )

    assert inspect_(note).is_well_formed()


def test_scoretools_Note___init___09():
    r'''Initializes note from rest.
    '''

    rest = Rest('r8')
    note = Note(rest)

    assert format(note) == stringtools.normalize(
        r'''
        8
        '''
        )

    assert inspect_(note).is_well_formed()


def test_scoretools_Note___init___10():
    r'''Initializes note from tupletized rest.
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
    r'''Initializes note from beamed rest.
    '''

    staff = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    beam = Beam()
    attach(beam, staff[:])
    note = Note(staff[1])

    assert isinstance(staff[1], Rest)
    assert isinstance(note, Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_scoretools_Note___init___12():
    r'''Initializes notes from skip.
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
    r'''Initializes note from tupletized skip.
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
    r'''Initializes note from beamed skip.
    '''

    staff = Staff([Note(0, (1, 8)), scoretools.Skip((1, 8)), Note(0, (1, 8))])
    beam = Beam()
    attach(beam, staff[:])
    note = Note(staff[1])

    assert isinstance(staff[1], scoretools.Skip)
    assert isinstance(note, Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_scoretools_Note___init___15():
    r'''Initializes note with cautionary accidental.
    '''

    note = Note("c'?4")

    assert format(note) == "c'?4"


def test_scoretools_Note___init___16():
    r'''Initializes note with forced accidental.
    '''

    note = Note("c'!4")

    assert format(note) == "c'!4"


def test_scoretools_Note___init___17():
    r'''Initializes note with both forced and cautionary accidental.
    '''

    note = Note("c'!?4")

    assert format(note) == "c'!?4"


def test_scoretools_Note___init___18():
    r'''Initializes note from chord with forced and cautionary accidental.
    '''

    chord = Chord("<c'!? e' g'>4")
    note = Note(chord)

    assert format(note) == "c'!?4"


def test_scoretools_Note___init___19():
    r'''Initialize note with drum pitch.
    '''

    note = Note('sn4')

    assert format(note) == 'snare4'
