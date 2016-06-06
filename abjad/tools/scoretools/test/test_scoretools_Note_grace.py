# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Note_grace_01():
    r'''Attach one grace note.
    '''

    note = Note("c'4")
    grace_container = scoretools.GraceContainer([Note(2, (1, 16))])
    attach(grace_container, note)

    assert format(note) == stringtools.normalize(
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
    grace_container = scoretools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
    attach(grace_container, note)

    assert format(note) == stringtools.normalize(
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
    grace_container = scoretools.GraceContainer([Note(2, (1, 16))], kind='appoggiatura')
    attach(grace_container, note)

    assert format(note) == stringtools.normalize(
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
    grace = scoretools.GraceContainer([Note(2, (1, 16))], kind='acciaccatura')
    attach(grace, note)

    assert format(note) == stringtools.normalize(
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
    grace = scoretools.GraceContainer([Note(2, (1, 16))], kind='after')
    attach(grace, note)

    assert format(note) == stringtools.normalize(
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
    grace = scoretools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))], kind='after')
    attach(grace, note)

    assert format(note) == stringtools.normalize(
        r'''
        \afterGrace
        c'4
        {
            c'16
            d'16
            e'16
        }
        '''
        )
