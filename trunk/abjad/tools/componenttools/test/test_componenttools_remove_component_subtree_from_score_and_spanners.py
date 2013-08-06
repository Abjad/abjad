# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_remove_component_subtree_from_score_and_spanners_01():
    r'''Detach sequential from score tree.
    '''

    t = Voice(notetools.make_repeated_notes(2))
    t.insert(1, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t.select_leaves())
    spannertools.GlissandoSpanner(t.select_leaves())

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

    sequential = t[1]
    componenttools.remove_component_subtree_from_score_and_spanners(t[1:2])

    r'''
    \new Voice {
        c'8 [ \glissando
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert select(sequential).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\tc'8 [ \\glissando\n\tf'8 ]\n}"
        )


def test_componenttools_remove_component_subtree_from_score_and_spanners_02():
    r'''Detach leaf from score tree.
    '''

    t = Voice(notetools.make_repeated_notes(2))
    t.insert(1, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t.select_leaves())
    spannertools.GlissandoSpanner(t.select_leaves())

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

    leaf = t.select_leaves()[1]
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

    assert select(t).is_well_formed()
    assert select(leaf).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\tc'8 [ \\glissando\n\t{\n\t\te'8 \\glissando\n\t}\n\tf'8 ]\n}"
        )
