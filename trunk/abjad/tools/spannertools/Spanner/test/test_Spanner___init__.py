# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Spanner___init___01():
    r'''Init empty spanner.
    '''

    beam = spannertools.BeamSpanner()
    assert len(beam) == 0
    assert beam[:] == []


def test_Spanner___init___02():
    r'''Init nonempty spanner.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(container[:])

    r'''
    {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert len(beam) == 4
    assert beam[:] == container[:]


def test_Spanner___init___03():
    r'''Spanner is abstract.
    '''

    assert py.test.raises(TypeError, 'beam = spannertools.Spanner()')
