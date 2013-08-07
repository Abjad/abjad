# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_01():
    r'''Flip leaf under continuous spanner.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(voice[1])

    r'''
    \new Voice {
        c'8 [
        e'8
        d'8
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            e'8
            d'8
            f'8 ]
        }
        '''
        )


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_02():
    r'''Flip leaf across spanner boundaries.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:2])
    spannertools.BeamSpanner(voice[2:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8 [
        f'8 ]
    }
    '''

    componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(voice[1])

    r'''
    \new Voice {
        c'8 [
        e'8 ]
        d'8 [
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            e'8 ]
            d'8 [
            f'8 ]
        }
        '''
        )


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_03():
    r'''Flip leaf from within to without spanner.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:2])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        e'8
        f'8
    }
    '''

    componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(voice[1])

    r'''
    \new Voice {
        c'8 [
        e'8 ]
        d'8
        f'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            e'8 ]
            d'8
            f'8
        }
        '''
        )


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_04():
    r'''Donate from empty container to leaf.
    '''

    voice = Voice([Container("c'8 d'8"), Container([])])
    spannertools.GlissandoSpanner(voice[:])
    spannertools.BeamSpanner(voice[:])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 ]
        }
        {
        }
    }
    '''

    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(voice[1:2], Note(4, (1, 8)))
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(voice[1:2], [Note(4, (1, 8))])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        e'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            e'8 ]
        }
        '''
        )


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_05():
    r'''Donate from empty container to nonempty container.
    '''

    voice = Voice([Container("c'8 d'8"), Container([])])
    spannertools.GlissandoSpanner(voice[:])
    spannertools.BeamSpanner(voice[:])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 ]
        }
        {
        }
    }
    '''

    container = Container([Note(4, (1, 8)), Note(5, (1, 8))])
    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(voice[1:2], container)
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(voice[1:2], [container])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 ]
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 ]
            }
        }
        '''
        )


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_06():
    r'''Donate from note to rest.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice.select_leaves())

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    old = voice.select_leaves()[2]
    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(voice.select_leaves()[2:3], Rest((1, 8)))
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(voice.select_leaves()[2:3], [Rest((1, 8))])

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            r8
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                r8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )


def test_componenttools_move_component_subtree_to_right_in_immediate_parent_of_component_07():
    r'''Donate from note to tuplet.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.GlissandoSpanner(voice[:])
    spannertools.BeamSpanner(voice.select_leaves())

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 \glissando
        }
        {
            g'8 \glissando
            a'8 ]
        }
    }
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 8), Note(0, (1, 16)) * 3)
    #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(voice[1][:1], tuplet)
    # ALSO WORKS:
    componenttools.move_parentage_and_spanners_from_components_to_components(voice[1][:1], [tuplet])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            \times 2/3 {
                c'16 \glissando
                c'16 \glissando
                c'16 \glissando
            }
            f'8 \glissando
        }
        {
            g'8 \glissando
            a'8 ]
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                \times 2/3 {
                    c'16 \glissando
                    c'16 \glissando
                    c'16 \glissando
                }
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )
