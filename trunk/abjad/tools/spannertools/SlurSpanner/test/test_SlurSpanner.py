# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner_01():
    r'''Slur spanner can attach to a container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(voice)

    r'''
    \new Voice {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert more(voice).get_spanners() == set([slur])
    assert testtools.compare(
        voice,
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

    voice = Voice("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(voice[:])

    assert len(more(voice).get_spanners()) == 0
    for leaf in voice.select_leaves():
        assert more(leaf).get_spanners() == set([slur])
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )
