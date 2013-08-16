# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_replace_components_with_children_of_components_01():
    r'''Containers can 'slip out' of score structure.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    beam = spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    sequential = staff[0]
    componenttools.replace_components_with_children_of_components(staff[0:1])

    r'''
    \new Staff {
        c'8 [
        d'8
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(sequential) == 0
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            {
                e'8
                f'8 ]
            }
        }
        '''
        )


def test_componenttools_replace_components_with_children_of_components_02():
    r'''Slip leaf from parentage and spanners.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    spannertools.GlissandoSpanner(voice[:])

    note = voice[1]
    componenttools.replace_components_with_children_of_components([note])

    r'''
    \new Voice {
        c'8 [ \glissando
        e'8 \glissando
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )


def test_componenttools_replace_components_with_children_of_components_03():
    r'''Slip multiple leaves.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    spannertools.GlissandoSpanner(voice[:])

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 \glissando
        e'8 \glissando
        f'8 ]
    }
    '''

    componenttools.replace_components_with_children_of_components(voice[:2])

    r'''
    \new Voice {
        e'8 [ \glissando
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            e'8 [ \glissando
            f'8 ]
        }
        '''
        )


def test_componenttools_replace_components_with_children_of_components_04():
    r'''Slip multiple containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice.select_leaves())
    spannertools.GlissandoSpanner(voice.select_leaves())

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

    componenttools.replace_components_with_children_of_components(voice[:2])

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 \glissando
        e'8 \glissando
        f'8 \glissando
        {
            g'8 \glissando
            a'8 ]
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 \glissando
            e'8 \glissando
            f'8 \glissando
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )
