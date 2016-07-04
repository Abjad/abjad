# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Selection__attach_tie_spanner_to_leaf_pair_01():
    r'''Span left leaf with spanner and right leaf without spanner.
    '''

    voice = Voice("c'8 c'8 c'8 c'8")
    tie = spannertools.Tie()
    attach(tie, voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8
            c'8
            c'8
        }
        '''
        )

    selector = select().by_leaf(flatten=True)
    leaves = selector(voice)
    leaves[1:3]._attach_tie_spanner_to_leaf_pair()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8 ~
            c'8
            c'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_selectiontools_Selection__attach_tie_spanner_to_leaf_pair_02():
    r'''Span left leaf with spanner and right leaf with spanner.
    '''

    voice = Voice("c'8 c'8 c'8 c'8")
    tie = spannertools.Tie()
    attach(tie, voice[:2])
    tie = spannertools.Tie()
    attach(tie, voice[2:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8
            c'8 ~
            c'8
        }
        '''
        )

    selector = select().by_leaf(flatten=True)
    leaves = selector(voice)
    leaves[1:3]._attach_tie_spanner_to_leaf_pair()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_selectiontools_Selection__attach_tie_spanner_to_leaf_pair_03():
    r'''Span left leaves with no spanner.
    '''

    voice = Voice("c'8 c'8 c'8 c'8")
    selector = select().by_leaf(flatten=True)
    leaves = selector(voice)
    leaves[1:3]._attach_tie_spanner_to_leaf_pair()

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8
            c'8 ~
            c'8
            c'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()