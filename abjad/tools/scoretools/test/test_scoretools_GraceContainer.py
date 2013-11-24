# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_GraceContainer_01():
    r'''Grace music is a container.
    '''

    gracecontainer = scoretools.GraceContainer(
        [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])

    assert systemtools.TestManager.compare(
        gracecontainer,
        r'''
        \grace {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert isinstance(gracecontainer, Container)
    assert len(gracecontainer) == 3


def test_scoretools_GraceContainer_02():
    r'''GraceContainer.kind is managed attribute.
    GraceContainer.kind knows about "after", "grace",
    "acciaccatura", "appoggiatura".
    '''

    gracecontainer = scoretools.GraceContainer(
        [Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
    gracecontainer.kind = 'acciaccatura'
    assert gracecontainer.kind == 'acciaccatura'
    gracecontainer.kind = 'grace'
    assert gracecontainer.kind == 'grace'
    gracecontainer.kind = 'after'
    assert gracecontainer.kind == 'after'
    gracecontainer.kind = 'appoggiatura'
    assert gracecontainer.kind == 'appoggiatura'
    assert pytest.raises(AssertionError, 'gracecontainer.kind = "blah"')


def test_scoretools_GraceContainer_03():
    r'''Grace formats correctly as grace.
    '''

    gracecontainer = scoretools.GraceContainer(scoretools.make_repeated_notes(3))
    gracecontainer.kind = 'grace'
    assert systemtools.TestManager.compare(
        gracecontainer,
        r'''
        \grace {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_04():
    r'''Grace formats correctly as acciaccatura.
    '''

    gracecontainer = scoretools.GraceContainer("c'8 c'8 c'8")
    gracecontainer.kind = 'acciaccatura'
    assert systemtools.TestManager.compare(
        gracecontainer,
        r'''
        \acciaccatura {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_05():
    r'''Grace formats correctly as appoggiatura.
    '''

    gracecontainer = scoretools.GraceContainer("c'8 c'8 c'8")
    gracecontainer.kind = 'appoggiatura'
    assert systemtools.TestManager.compare(
        gracecontainer,
        r'''
        \appoggiatura {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_06():
    r'''Grace formats correctly as after grace.
    '''

    gracecontainer = scoretools.GraceContainer("c'8 c'8 c'8")
    gracecontainer.kind = 'after'
    assert systemtools.TestManager.compare(
        gracecontainer,
        r'''
        {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_07():
    r'''Grace containers can be appended.
    '''

    gracecontainer = scoretools.GraceContainer("c'8 c'8")
    note = Note(1, (1, 4))
    gracecontainer.append(note)
    assert len(gracecontainer) == 3
    assert gracecontainer[-1] is note


def test_scoretools_GraceContainer_08():
    r'''Grace containers can be extended.
    '''

    gracecontainer = scoretools.GraceContainer("c'8 c'8")
    ns = Note(1, (1, 4)) * 2
    gracecontainer.extend(ns)
    assert len(gracecontainer) == 4
    assert tuple(gracecontainer[-2:]) == tuple(ns)
