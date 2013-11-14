# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Container___init___01():
    r'''Initializeempty container.
    '''

    container = Container([])

    r'''
    {
    }
    '''

    assert isinstance(container, Container)
    assert systemtools.TestManager.compare(
        container,
        r'''
        {
        }
        '''
        )


def test_scoretools_Container___init___02():
    r'''Initializecontainer with LilyPond note-entry string.
    '''

    container = Container("c'8 d'8 e'8")

    r'''
    {
        c'8
        d'8
        e'8
    }
    '''

    assert isinstance(container, Container)
    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8
            d'8
            e'8
        }
        '''
        )


def test_scoretools_Container___init___03():
    r'''Initializecontainer with RTM-syntax string.
    '''

    container = Container('rtm: (1 (1 1 1)) (2 (2 (1 (1 1 1)) 2))')

    r'''
    {
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        \times 4/5 {
            c'4
            \times 2/3 {
                c'16
                c'16
                c'16
            }
            c'4
        }
    }
    '''

    assert isinstance(container, Container)
    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            \times 2/3 {
                c'8
                c'8
                c'8
            }
            \times 4/5 {
                c'4
                \times 2/3 {
                    c'16
                    c'16
                    c'16
                }
                c'4
            }
        }
        '''
        )

def test_scoretools_Container___init___04():
    r'''Initializecontainer with "reduced ly" syntax string.
    '''

    container = Container('abj: 2/3 { 8 8 8 }')

    r'''
    \times 2/3 {
        c'8
        c'8
        c'8
    }
    '''

    assert isinstance(container, Container)
    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            \times 2/3 {
                c'8
                c'8
                c'8
            }
        }
        '''
        )
