# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_GraceContainer_01():
    r'''Grace music is a container.
    '''

    t = leaftools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])

    assert isinstance(t, Container)
    assert len(t) == 3
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \grace {
            c'16
            d'16
            e'16
        }
        '''
        )

    r'''
    \grace {
        c'16
        d'16
        e'16
    }
    '''


def test_GraceContainer_02():
    r'''GraceContainer.kind is managed attribute.
        GraceContainer.kind knows about "after", "grace",
        "acciaccatura", "appoggiatura"'''

    t = leaftools.GraceContainer([Note(0, (1, 16)), Note(2, (1, 16)), Note(4, (1, 16))])
    t.kind = 'acciaccatura'
    assert t.kind == 'acciaccatura'
    t.kind = 'grace'
    assert t.kind == 'grace'
    t.kind = 'after'
    assert t.kind == 'after'
    t.kind = 'appoggiatura'
    assert t.kind == 'appoggiatura'
    assert py.test.raises(AssertionError, 't.kind = "blah"')


def test_GraceContainer_03():
    r'''Grace formats correctly as grace.
    '''

    t = leaftools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'grace'
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \grace {
            c'8
            c'8
            c'8
        }
        '''
        )

    r'''
    \grace {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_04():
    r'''Grace formats correctly as acciaccatura.
    '''

    t = leaftools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'acciaccatura'
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \acciaccatura {
            c'8
            c'8
            c'8
        }
        '''
        )

    r'''
    \acciaccatura {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_05():
    r'''Grace formats correctly as appoggiatura.
    '''

    t = leaftools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'appoggiatura'
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \appoggiatura {
            c'8
            c'8
            c'8
        }
        '''
        )

    r'''
    \appoggiatura {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_06():
    r'''Grace formats correctly as after grace.
    '''

    t = leaftools.GraceContainer(notetools.make_repeated_notes(3))
    t.kind = 'after'
    assert testtools.compare(
        t.lilypond_format,
        r'''
        {
            c'8
            c'8
            c'8
        }
        '''
        )

    r'''
    {
        c'8
        c'8
        c'8
    }
    '''


def test_GraceContainer_07():
    r'''Grace containers can be appended.
    '''

    t = leaftools.GraceContainer(notetools.make_repeated_notes(2))
    n = Note(1, (1, 4))
    t.append(n)
    assert len(t) == 3
    assert t[-1] is n


def test_GraceContainer_08():
    r'''Grace containers can be extended.
    '''

    t = leaftools.GraceContainer(notetools.make_repeated_notes(2))
    ns = Note(1, (1, 4)) * 2
    t.extend(ns)
    assert len(t) == 4
    assert t[-2:] == ns
