# -*- coding: utf-8 -*-
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
    r'''Initialize rest from chord.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    rest = Rest(chord)

    assert isinstance(rest, Rest)
    assert dir(chord) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(rest) == dir(Rest((1, 4)))
    assert rest.written_duration == chord.written_duration


def test_scoretools_Rest___init___04():
    r'''Initialize rest from tupletized chord.
    '''

    chord = Chord([2, 3, 4], Duration(1, 4))
    tuplet = Tuplet((2, 3), 3 * chord)
    rest = Rest(tuplet[0])

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        ''',
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___05():
    r'''Initialize rest from beamed chord.
    '''

    chord = Chord([2, 3, 4], Duration(1, 4))
    staff = Staff(3 * chord)
    beam = Beam()
    attach(beam, staff[:])
    rest = Rest(staff[0])

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        ''',
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___06():
    r'''Initialize rest from skip.
    '''

    skip = scoretools.Skip('s4')
    rest = Rest(skip)

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        ''',
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___07():
    r'''Initialize rest from tupletted skip.
    '''

    skip = scoretools.Skip('s4')
    tuplet = Tuplet((2, 3), 3 * skip)
    rest = Rest(tuplet[0])

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        ''',
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___08():
    r'''Initialize rest from beamed skip.
    '''

    skip = scoretools.Skip('s8')
    staff = Staff("c'8 [ s4 c'd ]")
    rest = Rest(staff[1])

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        '''
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___09():
    r'''Initialize rest from note.
    '''

    note = Note("c'4")
    rest = Rest(note)

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        '''
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___10():
    r'''Initialize rest from tupletized note.
    '''

    tuplet = Tuplet((2, 3), "c'4 d'4 e'4")
    rest = Rest(tuplet[0])

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        '''
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___11():
    r'''Initialize rest from beamed note.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")
    rest = Rest(staff[0])

    assert format(rest) == stringtools.normalize(
        r'''
        r8
        '''
        )

    assert inspect_(rest).is_well_formed()


def test_scoretools_Rest___init___12():
    r'''Initialize multiple rests from spanned notes.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    for note in voice:
        rest = Rest(note)
        mutate(note).replace(rest)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            r8 [
            r8
            r8
            r8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Rest___init___13():
    '''Initializes rest from empty input.
    '''

    rest = Rest()

    assert format(rest) == stringtools.normalize(
        r'''
        r4
        '''
        )

    assert inspect_(rest).is_well_formed()
