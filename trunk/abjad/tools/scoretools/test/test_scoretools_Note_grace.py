# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Note_grace_01():
    r'''Attach one grace note.
    '''

    note = Note("c'4")
    scoretools.GraceContainer([Note(2, (1, 16))])(note)

    '''
    \grace {
        d'16
    }
    c'4
    '''

    assert testtools.compare(
        note,
        r'''
        \grace {
            d'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_02():
    r'''Attach several grace notes.
    '''

    note = Note("c'4")
    scoretools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])(note)

    '''
    \grace {
        c'16
        d'16
        e'16
    }
    c'4
    '''

    assert testtools.compare(
        note,
        r'''
        \grace {
            c'16
            d'16
            e'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_03():
    r'''Attach one appoggiatura.
    '''

    note = Note("c'4")
    scoretools.GraceContainer([Note(2, (1, 16))], kind = 'appoggiatura')(note)

    r'''
    \appoggiatura {
        d'16
    }
    c'4
    '''

    assert testtools.compare(
        note,
        r'''
        \appoggiatura {
            d'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_04():
    r'''Attach one acciaccatura.
    '''

    note = Note("c'4")
    scoretools.GraceContainer([Note(2, (1, 16))], kind = 'acciaccatura')(note)

    r'''
    \acciaccatura {
        d'16
    }
    c'4
    '''

    assert testtools.compare(
        note,
        r'''
        \acciaccatura {
            d'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_05():
    r'''Attach one after grace note.
    '''

    note = Note("c'4")
    scoretools.GraceContainer([Note(2, (1, 16))], kind = 'after')(note)

    r'''
    \afterGrace
    c'4
    {
        d'16
    }
    '''

    assert testtools.compare(
        note,
        r'''
        \afterGrace
        c'4
        {
            d'16
        }
        '''
        )


def test_scoretools_Note_grace_06():
    r'''Attach several after grace notes.
    '''

    note = Note("c'4")
    scoretools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))], kind = 'after')(note)

    r'''
    \afterGrace
    c'4
    {
        c'16
        d'16
        e'16
    }
    '''

    assert format(note) =="\\afterGrace\nc'4\n{\n\tc'16\n\td'16\n\te'16\n}"
