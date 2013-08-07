# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_remove_component_subtree_from_score_and_spanners_01():
    r'''Detach sequential from score tree.
    '''

    voice = Voice(notetools.make_repeated_notes(2))
    voice.insert(1, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice.select_leaves())
    spannertools.GlissandoSpanner(voice.select_leaves())

    r'''
    \new Voice {
        c'8 [ \glissando
        {
            d'8 \glissando
            e'8 \glissando
        }
        f'8 ]
    }
    '''

    sequential = voice[1]
    componenttools.remove_component_subtree_from_score_and_spanners(voice[1:2])

    r'''
    \new Voice {
        c'8 [ \glissando
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert select(sequential).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 [ \glissando
            f'8 ]
        }
        '''
        )


def test_componenttools_remove_component_subtree_from_score_and_spanners_02():
    r'''Detach leaf from score tree.
    '''

    voice = Voice(notetools.make_repeated_notes(2))
    voice.insert(1, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice.select_leaves())
    spannertools.GlissandoSpanner(voice.select_leaves())

    r'''
    \new Voice {
        c'8 [ \glissando
        {
            d'8 \glissando
            e'8 \glissando
        }
        f'8 ]
    }
    '''

    leaf = voice.select_leaves()[1]
    componenttools.remove_component_subtree_from_score_and_spanners([leaf])

    r'''
    \new Voice {
        c'8 [ \glissando
        {
            e'8 \glissando
        }
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert select(leaf).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                e'8 \glissando
            }
            f'8 ]
        }
        '''
        )
