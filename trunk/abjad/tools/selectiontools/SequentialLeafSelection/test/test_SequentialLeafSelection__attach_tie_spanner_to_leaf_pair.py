# -*- encoding: utf-8 -*-
from abjad import *


def test_SequentialLeafSelection__attach_tie_spanner_to_leaf_pair_01():
    r'''Span left leaf with spanner and right leaf without spanner.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(voice[:2])

    r'''
    \new Voice {
        c'8 ~
        c'8
        c'8
        c'8
    }
    '''

    voice.select_leaves()[1:3]._attach_tie_spanner_to_leaf_pair()

    r'''
    \new Voice {
        c'8 ~
        c'8 ~
        c'8
        c'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 ~
            c'8 ~
            c'8
            c'8
        }
        '''
        )


def test_SequentialLeafSelection__attach_tie_spanner_to_leaf_pair_02():
    r'''Span left leaf with spanner and right leaf with spanner.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(voice[:2])
    spannertools.TieSpanner(voice[2:])

    r'''
    \new Voice {
        c'8 ~
        c'8
        c'8 ~
        c'8
    }
    '''

    voice.select_leaves()[1:3]._attach_tie_spanner_to_leaf_pair()

    r'''
    \new Voice {
        c'8 ~
        c'8 ~
        c'8 ~
        c'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }
        '''
        )


def test_SequentialLeafSelection__attach_tie_spanner_to_leaf_pair_03():
    r'''Span left leaves with no spanner.
    '''

    t = Voice(notetools.make_repeated_notes(4))

    r'''
    \new Voice {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    t.select_leaves()[1:3]._attach_tie_spanner_to_leaf_pair()

    r'''
    \new Voice {
        c'8
        c'8 ~
        c'8
        c'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8
            c'8 ~
            c'8
            c'8
        }
        '''
        )
