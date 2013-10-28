# -*- encoding: utf-8 -*-
from abjad import *


def test_resttools_Rest___init___01():
    r'''Init rest from LilyPond input string.
    '''

    rest = Rest('r8.')

    assert rest.written_duration == Duration(3, 16)


def test_resttools_Rest___init___02():
    r'''Init rest from written duration and LilyPond multiplier.
    '''

    rest = Rest(Duration(1, 4), Duration(1, 2))

    assert rest.lilypond_format == 'r4 * 1/2'


def test_resttools_Rest___init___03():
    r'''Init rest from other rest.
    '''

    rest_1 = Rest((1, 4), (1, 2))
    rest_1.override.staff.note_head.color = 'red'
    rest_2 = Rest(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert rest_1.lilypond_format == rest_2.lilypond_format
    assert rest_1 is not rest_2


def test_resttools_Rest___init___04():
    r'''Init rest from containerized chord.
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


def test_resttools_Rest___init___05():
    r'''Init rest from tupletized chord.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = tuplet[0].written_duration
    rest = Rest(tuplet[0])
    assert isinstance(rest, Rest)
    assert isinstance(tuplet[0], Chord)
    assert tuplet[0]._parent is tuplet
    assert rest._parent is None


def test_resttools_Rest___init___06():
    r'''Init rest from beamed chord.
    '''

    staff = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    beam = spannertools.BeamSpanner()
    beam.attach(staff[:])
    rest = Rest(staff[0])
    assert isinstance(rest, Rest)
    assert isinstance(staff[0], Chord)
    assert staff[0]._parent is staff
    assert rest._parent is None


def test_resttools_Rest___init___07():
    r'''Init rest from skip.
    '''

    skip = skiptools.Skip((1, 8))
    d = skip.written_duration
    rest = Rest(skip)
    assert isinstance(rest, Rest)
    assert dir(skip) == dir(skiptools.Skip((1, 4)))
    assert dir(rest) == dir(Rest((1, 4)))
    assert rest._parent is None
    assert rest.written_duration == d


def test_resttools_Rest___init___08():
    r'''Init rest from tupletted skip.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), skiptools.Skip((1, 8)) * 3)
    d = tuplet[0].written_duration
    rest = Rest(tuplet[0])
    assert isinstance(tuplet[0], skiptools.Skip)
    assert isinstance(rest, Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert rest._parent is None


def test_resttools_Rest___init___09():
    r'''Init rest from beamed skip.
    '''

    staff = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
    beam = spannertools.BeamSpanner()
    beam.attach(staff[:])
    rest = Rest(staff[1])
    assert isinstance(staff[1], skiptools.Skip)
    assert staff[1] in staff
    assert isinstance(rest, Rest)
    assert rest not in staff


def test_resttools_Rest___init___10():
    r'''Init rest from unincorporated note.
    '''

    note = Note(2, (1, 8))
    d = note.written_duration
    rest = Rest(note)
    assert isinstance(rest, Rest)
    # check that attributes have not been removed or added.
    assert dir(note) == dir(Note(0, (1, 8)))
    assert dir(rest) == dir(Rest((1, 4)))
    assert rest.lilypond_format == 'r8'
    assert rest._parent is None
    assert rest.written_duration == d


def test_resttools_Rest___init___11():
    r'''Init rest from tupletized note.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    d = tuplet[0].written_duration
    rest = Rest(tuplet[0])
    assert isinstance(tuplet[0], Note)
    assert isinstance(rest, Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == d
    assert rest._parent is None


def test_resttools_Rest___init___12():
    r'''Init rest from beamed note.
    '''

    staff = Staff(Note(0, (1, 8)) * 3)
    beam = spannertools.BeamSpanner()
    beam.attach(staff[:])
    rest = Rest(staff[0])
    assert isinstance(staff[0], Note)
    assert isinstance(rest, Rest)
    assert staff[0]._parent is staff
    assert rest._parent is None


def test_resttools_Rest___init___13():
    r'''Init rest from spanned note.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
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


def test_resttools_Rest___init___14():
    r'''Init multiple rests from spanned notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
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
