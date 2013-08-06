# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner_01():
    r'''Slur spanner can attach to a container.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    s = spannertools.SlurSpanner(t)

    r'''
    \new Voice {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert t.get_spanners() == set([s])
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )


def test_SlurSpanner_02():
    r'''Slur spanner can attach to leaves.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    s = spannertools.SlurSpanner(t[:])

    assert len(t.get_spanners()) == 0
    for leaf in t.select_leaves():
        assert leaf.get_spanners() == set([s])
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )
