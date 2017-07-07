# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Note_grace_01():
    r'''Attaches one grace note.
    '''

    note = Note("c'4")
    grace_container = GraceContainer([Note(2, (1, 16))])
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
    r'''Attaches several grace notes.
    '''

    note = Note("c'4")
    grace_notes = [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))]
    grace_container = GraceContainer(grace_notes)
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
    r'''Attaches one appoggiatura.
    '''

    note = Note("c'4")
    grace_container = AppoggiaturaContainer([Note(2, (1, 16))])
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
    r'''Attaches one acciaccatura.
    '''

    note = Note("c'4")
    grace = AcciaccaturaContainer([Note(2, (1, 16))])
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
    r'''Attaches one after grace note.
    '''

    note = Note("c'4")
    grace = AfterGraceContainer([Note(2, (1, 16))])
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
    r'''Attaches several after grace notes.
    '''

    note = Note("c'4")
    grace_notes = [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))]
    grace = AfterGraceContainer(grace_notes)
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
