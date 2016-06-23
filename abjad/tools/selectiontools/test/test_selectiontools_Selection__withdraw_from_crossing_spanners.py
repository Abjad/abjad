# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_selectiontools_Selection__withdraw_from_crossing_spanners_01():
    r'''Withdraw components from crossing spanners.
    No spanners cross voice.
    '''

    voice = Voice(r'''
        {
            c'8 [ \startTrillSpan
            d'8 ]
        }
        {
            e'8 (
            f'8 ) \stopTrillSpan
        }
        ''')

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8 ]
            }
            {
                e'8 (
                f'8 ) \stopTrillSpan
            }
        }
        '''
        )

    voice_selection = selectiontools.Selection([voice])
    voice_selection._withdraw_from_crossing_spanners()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8 ]
            }
            {
                e'8 (
                f'8 ) \stopTrillSpan
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_selectiontools_Selection__withdraw_from_crossing_spanners_02():
    r'''Withdraw logical-voice-contiguous components from crossing spanners.
    '''

    voice = Voice(r'''
        {
            c'8 [ \startTrillSpan
            d'8 ]
        }
        {
            e'8 (
            f'8 ) \stopTrillSpan
        }
        ''')

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8 ]
            }
            {
                e'8 (
                f'8 ) \stopTrillSpan
            }
        }
        '''
        )

    voice[:1]._withdraw_from_crossing_spanners()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [
                d'8 ]
            }
            {
                e'8 ( \startTrillSpan
                f'8 ) \stopTrillSpan
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_selectiontools_Selection__withdraw_from_crossing_spanners_03():
    r'''Withdraw logical-voice-contiguous components from crossing spanners.
    Operation leaves score tree in weird state.
    Both slur and trill become discontiguous.
    '''

    voice = Voice(r'''
        {
            c'8 [ \startTrillSpan
            d'8 ]
        }
        {
            e'8 (
            f'8 ) \stopTrillSpan
        }
        ''')

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8 ]
            }
            {
                e'8 (
                f'8 ) \stopTrillSpan
            }
        }
        '''
        )

    selector = select().by_leaf(flatten=True)
    leaves = selector(voice)
    leaves[2:3]._withdraw_from_crossing_spanners()
    assert not inspect_(voice).is_well_formed()