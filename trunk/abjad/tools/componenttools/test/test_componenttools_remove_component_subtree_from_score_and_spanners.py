from abjad import *


def test_componenttools_remove_component_subtree_from_score_and_spanners_01():
    '''Detach sequential from score tree.'''

    t = Voice(notetools.make_repeated_notes(2))
    t.insert(1, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)
    spannertools.GlissandoSpanner(t.leaves)

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

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(sequential)
    assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\tf'8 ]\n}"


def test_componenttools_remove_component_subtree_from_score_and_spanners_02():
    '''Detach leaf from score tree.'''

    t = Voice(notetools.make_repeated_notes(2))
    t.insert(1, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)
    spannertools.GlissandoSpanner(t.leaves)

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

    leaf = t.leaves[1]
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

    assert componenttools.is_well_formed_component(t)
    assert componenttools.is_well_formed_component(leaf)
    assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\t{\n\t\te'8 \\glissando\n\t}\n\tf'8 ]\n}"
