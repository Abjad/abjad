# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_spannertools_Spanner___init___01():
    r'''Initializeempty spanner.
    '''

    beam = Beam()
    assert len(beam) == 0
    assert beam[:] == []


def test_spannertools_Spanner___init___02():
    r'''Initializenonempty spanner.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, container[:])

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert len(beam) == 4
    assert beam[:] == container[:]


def test_spannertools_Spanner___init___03():
    r'''Spanner is abstract.
    '''

    assert pytest.raises(TypeError, 'beam = spannertools.Spanner()')
