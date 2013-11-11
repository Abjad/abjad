# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Rest___init___01():
    r'''Initialize rest from LilyPond input string.
    '''

    rest = Rest('r8.')

    assert rest.written_duration == Duration(3, 16)


def test_scoretools_Rest___init___02():
    r'''Initialize rest from other rest.
    '''

    rest_1 = Rest('r4')
    attach(Multiplier(1, 2), rest_1)
    override(rest_1).staff.note_head.color = 'red'
    rest_2 = Rest(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert format(rest_1) == format(rest_2)
    assert rest_1 is not rest_2


def test_scoretools_Rest___init___03():
    r'''Initialize rest from containerized chord.
    '''

    c = Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    rest = Rest(c)
    assert isinstance(rest, Rest)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(rest) == dir(Rest((1, 4)))
    assert rest._parent is None
    assert rest.written_duration == duration


def test_scoretools_Rest___init___04():
    r'''Initialize rest from tupletized chord.
    '''

    tuplet = scoretools.FixedDurationTuplet(
        Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = tuplet[0].written_duration
    rest = Rest(tuplet[0])
    assert isinstance(rest, Rest)
    assert isinstance(tuplet[0], Chord)
    assert tuplet[0]._parent is tuplet
    assert rest._parent is None


def test_scoretools_Rest___init___05():
    r'''Initialize rest from beamed chord.
    '''

    staff = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    beam = Beam()
    attach(beam, staff[:])
    rest = Rest(staff[0])
    assert isinstance(rest, Rest)
    assert isinstance(staff[0], Chord)
    assert staff[0]._parent is staff
    assert rest._parent is None


def test_scoretools_Rest___init___06():
    r'''Initialize rest from skip.
    '''

    skip = scoretools.Skip((1, 8))
    d = skip.written_duration
    rest = Rest(skip)
    assert isinstance(rest, Rest)
    assert dir(skip) == dir(scoretools.Skip((1, 4)))
    assert dir(rest) == dir(Rest((1, 4)))
    assert rest._parent is None
    assert rest.written_duration == d


def test_scoretools_Rest___init___07():
    r'''Initialize rest from tupletted skip.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), scoretools.Skip((1, 8)) * 3)
    d = tuplet[0].written_duration
    rest = Rest(tuplet[0])
    assert isinstance(tuplet[0], scoretools.Skip)
    assert isinstance(rest, Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert rest._parent is None


def test_scoretools_Rest___init___08():
    r'''Initialize rest from beamed skip.
    '''

    staff = Staff([Note(0, (1, 8)), scoretools.Skip((1, 8)), Note(0, (1, 8))])
    beam = Beam()
    attach(beam, staff[:])
    rest = Rest(staff[1])
    assert isinstance(staff[1], scoretools.Skip)
    assert staff[1] in staff
    assert isinstance(rest, Rest)
    assert rest not in staff


def test_scoretools_Rest___init___09():
    r'''Initialize rest from unincorporated note.
    '''

    note = Note(2, (1, 8))
    d = note.written_duration
    rest = Rest(note)
    assert isinstance(rest, Rest)
    # check that attributes have not been removed or added.
    assert dir(note) == dir(Note(0, (1, 8)))
    assert dir(rest) == dir(Rest((1, 4)))
    assert format(rest) == 'r8'
    assert rest._parent is None
    assert rest.written_duration == d


def test_scoretools_Rest___init___10():
    r'''Initialize rest from tupletized note.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    d = tuplet[0].written_duration
    rest = Rest(tuplet[0])
    assert isinstance(tuplet[0], Note)
    assert isinstance(rest, Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert rest._parent is None


def test_scoretools_Rest___init___11():
    r'''Initialize rest from beamed note.
    '''

    staff = Staff(Note(0, (1, 8)) * 3)
    beam = Beam()
    attach(beam, staff[:])
    rest = Rest(staff[0])
    assert isinstance(staff[0], Note)
    assert isinstance(rest, Rest)
    assert staff[0]._parent is staff
    assert rest._parent is None


def test_scoretools_Rest___init___12():
    r'''Initialize rest from spanned note.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    rest = Rest(voice[-1])
    voice[-1:] = [rest]

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            r8 ]
        }
        '''
        )


def test_scoretools_Rest___init___13():
    r'''Initialize multiple rests from spanned notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    for note in voice:
        rest = Rest(note)
        mutate(note).replace(rest)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            r8 [
            r8
            r8
            r8 ]
        }
        '''
        )
