# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Container_is_simultaneous_01():
    r'''Is true when container encloses contents in LilyPond << >> brackets,
    otherwise False.
    '''

    assert not Container().is_simultaneous
    assert not scoretools.FixedDurationTuplet().is_simultaneous
    assert not Tuplet().is_simultaneous
    assert not Measure().is_simultaneous
    assert Score().is_simultaneous
    assert not Container().is_simultaneous
    assert not Staff().is_simultaneous
    assert scoretools.StaffGroup().is_simultaneous
    assert not Voice().is_simultaneous


def test_scoretools_Container_is_simultaneous_02():
    r'''Is true when container encloses contents in LilyPond << >> brackets,
    otherwise False.
    '''

    container = Container([])
    container.is_simultaneous = True
    assert container.is_simultaneous


def test_scoretools_Container_is_simultaneous_03():
    r'''Container 'simultaneous' is settable.
    '''

    container = Container([])
    assert not container.is_simultaneous

    container.is_simultaneous = True
    assert container.is_simultaneous


def test_scoretools_Container_is_simultaneous_04():
    r'''A simultaneous container can hold Contexts.
    '''

    container = Container([Voice("c'8 cs'8"), Voice("d'8 ef'8")])
    container.is_simultaneous = True

    assert format(container) == stringtools.normalize(
        r'''
        <<
            \new Voice {
                c'8
                cs'8
            }
            \new Voice {
                d'8
                ef'8
            }
        >>
        '''
        )


def test_scoretools_Container_is_simultaneous_05():
    r'''Simultaneous containers must contain only contexts.
    '''

    container = Container("c'8 c'8 c'8 c'8")
    pytest.raises(Exception, 'container.is_simultaneous = True')


def test_scoretools_Container_is_simultaneous_06():
    r'''Simultaneous containers must contain only Contexts.
    '''

    container = Container(2 * Container("c'8 c'8 c'8 c'8"))
    pytest.raises(Exception, 'container.is_simultaneous = True')
