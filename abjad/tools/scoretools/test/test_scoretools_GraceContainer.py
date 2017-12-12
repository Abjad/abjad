import abjad
import pytest


def test_scoretools_GraceContainer_01():

    notes = [abjad.Note(0, (1, 16)), abjad.Note(2, (1, 16)), abjad.Note(4, (1, 16))]
    grace_container = abjad.GraceContainer(notes)

    assert format(grace_container) == abjad.String.normalize(
        r'''
        \grace {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert isinstance(grace_container, abjad.Container)
    assert len(grace_container) == 3



def test_scoretools_GraceContainer_02():

    grace_container = abjad.GraceContainer("c'8 c'8 c'8")
    assert format(grace_container) == abjad.String.normalize(
        r'''
        \grace {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_03():

    grace_container = abjad.AcciaccaturaContainer("c'8 c'8 c'8")
    assert format(grace_container) == abjad.String.normalize(
        r'''
        \acciaccatura {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_04():

    grace_container = abjad.AppoggiaturaContainer("c'8 c'8 c'8")
    assert format(grace_container) == abjad.String.normalize(
        r'''
        \appoggiatura {
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_GraceContainer_05():

    grace_container = abjad.AfterGraceContainer("c'8 c'8 c'8")
    assert format(grace_container) == abjad.String.normalize(
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

    grace_container = abjad.GraceContainer("c'8 c'8")
    note = abjad.Note(1, (1, 4))
    grace_container.append(note)
    assert len(grace_container) == 3
    assert grace_container[-1] is note


def test_scoretools_GraceContainer_07():
    r'''Grace containers can be extended.
    '''

    grace_container = abjad.GraceContainer("c'8 c'8")
    ns = abjad.Note(1, (1, 4)) * 2
    grace_container.extend(ns)
    assert len(grace_container) == 4
    assert tuple(grace_container[-2:]) == tuple(ns)
