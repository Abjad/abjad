# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_Selection__attach_tie_spanner_to_leaf_pair_01():
    r'''Span left leaf with spanner and right leaf without spanner.
    '''

    voice = abjad.Voice("c'8 c'8 c'8 c'8")
    tie = abjad.Tie()
    abjad.attach(tie, voice[:2])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8
            c'8
            c'8
        }
        '''
        )

    selector = abjad.select().by_leaf(flatten=True)
    leaves = selector(voice)
    leaves[1:3]._attach_tie_spanner_to_leaf_pair()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8 ~
            c'8
            c'8
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_selectiontools_Selection__attach_tie_spanner_to_leaf_pair_02():
    r'''Span left leaf with spanner and right leaf with spanner.
    '''

    voice = abjad.Voice("c'8 c'8 c'8 c'8")
    tie = abjad.Tie()
    abjad.attach(tie, voice[:2])
    tie = abjad.Tie()
    abjad.attach(tie, voice[2:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8
            c'8 ~
            c'8
        }
        '''
        )

    selector = abjad.select().by_leaf(flatten=True)
    leaves = selector(voice)
    leaves[1:3]._attach_tie_spanner_to_leaf_pair()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_selectiontools_Selection__attach_tie_spanner_to_leaf_pair_03():
    r'''Span left leaves with no spanner.
    '''

    voice = abjad.Voice("c'8 c'8 c'8 c'8")
    selector = abjad.select().by_leaf(flatten=True)
    leaves = selector(voice)
    leaves[1:3]._attach_tie_spanner_to_leaf_pair()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8
            c'8 ~
            c'8
            c'8
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()