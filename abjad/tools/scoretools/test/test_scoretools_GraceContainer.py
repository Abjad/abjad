# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_GraceContainer_01():
    r'''Grace music is a container.
    '''

    notes = [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))]
    grace_container = GraceContainer(notes)

    assert format(grace_container) == stringtools.normalize(
        r'''
        \grace {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert isinstance(grace_container, Container)
    assert len(grace_container) == 3



def test_scoretools_GraceContainer_02():

    grace_container = GraceContainer("c'8 c'8 c'8")
    assert format(grace_container) == stringtools.normalize(
        r'''
        \grace {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_03():

    grace_container = AcciaccaturaContainer("c'8 c'8 c'8")
    assert format(grace_container) == stringtools.normalize(
        r'''
        \acciaccatura {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_04():

    grace_container = AppoggiaturaContainer("c'8 c'8 c'8")
    assert format(grace_container) == stringtools.normalize(
        r'''
        \appoggiatura {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_05():

    grace_container = AfterGraceContainer("c'8 c'8 c'8")
    assert format(grace_container) == stringtools.normalize(
        r'''
        {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_06():
    r'''Grace containers can be appended.
    '''

    grace_container = GraceContainer("c'8 c'8")
    note = Note(1, (1, 4))
    grace_container.append(note)
    assert len(grace_container) == 3
    assert grace_container[-1] is note


def test_scoretools_GraceContainer_07():
    r'''Grace containers can be extended.
    '''

    grace_container = GraceContainer("c'8 c'8")
    ns = Note(1, (1, 4)) * 2
    grace_container.extend(ns)
    assert len(grace_container) == 4
    assert tuple(grace_container[-2:]) == tuple(ns)
