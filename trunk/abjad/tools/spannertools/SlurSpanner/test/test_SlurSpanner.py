# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner_01():
    r'''Slur spanner can attach to a container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    s = spannertools.SlurSpanner(voice)

    r'''
    \new Voice {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert voice.get_spanners() == set([s])
    assert testtools.compare(
        voice.lilypond_format,
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
    s = spannertools.SlurSpanner(voice[:])

    assert len(voice.get_spanners()) == 0
    for leaf in voice.select_leaves():
        assert leaf.get_spanners() == set([s])
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )
