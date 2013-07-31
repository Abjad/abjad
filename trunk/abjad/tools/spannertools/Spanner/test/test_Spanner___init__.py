# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Spanner___init___01():
    r'''Init empty spanner.
    '''

    p = spannertools.BeamSpanner()
    assert len(p) == 0
    assert p[:] == []


def test_Spanner___init___02():
    r'''Init nonempty spanner.
    '''

    t = Container("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(t[:])

    r'''
    {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert len(p) == 4
    assert p[:] == t[:]


def test_Spanner___init___03():
    r'''Spanner is abstract.
    '''

    assert py.test.raises(TypeError, 'p = spannertools.Spanner()')
