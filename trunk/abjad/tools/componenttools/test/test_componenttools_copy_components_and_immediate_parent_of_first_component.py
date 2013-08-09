# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_copy_components_and_immediate_parent_of_first_component_01():
    r'''Copy adjacent notes in staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    u = componenttools.copy_components_and_immediate_parent_of_first_component(staff[:2])

    r'''
    \new Staff {
        c'8
        d'8
    }
    '''

    assert select(staff).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u,
        r'''
        \new Staff {
            c'8
            d'8
        }
        '''
        )


def test_componenttools_copy_components_and_immediate_parent_of_first_component_02():
    r'''Copy adjacent notes in staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    u = componenttools.copy_components_and_immediate_parent_of_first_component(staff[-2:])

    r'''
    \new Staff {
        e'8
        f'8
    }
    '''

    assert select(staff).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u,
        r'''
        \new Staff {
            e'8
            f'8
        }
        '''
        )



def test_componenttools_copy_components_and_immediate_parent_of_first_component_03():
    r'''Copy notes from tuplet and adjust tuplet target duration
    in order to preserve tuplet multiplier.'''

    tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8 f'8 g'8")
    u = componenttools.copy_components_and_immediate_parent_of_first_component(tuplet[:3])

    r'''
    \times 4/5 {
        c'8
        d'8
        e'8
    }
    '''

    assert isinstance(u, tuplettools.FixedDurationTuplet)
    assert u.target_duration == Duration(3, 10)
    assert len(u) == 3

    assert testtools.compare(
        u,
        r'''
        \times 4/5 {
            c'8
            d'8
            e'8
        }
        '''
        )


def test_componenttools_copy_components_and_immediate_parent_of_first_component_04():
    r'''Copy adjacent, whole tuplets from staff.
    '''

    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    u = componenttools.copy_components_and_immediate_parent_of_first_component(staff[1:])

    r'''
    \new Staff {
        \times 2/3 {
            f'8
            g'8
            a'8
        }
        \times 2/3 {
            b'8
            c''8
            d''8
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert select(u).is_well_formed()
    assert testtools.compare(
        u,
        r'''
        \new Staff {
            \times 2/3 {
                f'8
                g'8
                a'8
            }
            \times 2/3 {
                b'8
                c''8
                d''8
            }
        }
        '''
        )


def test_componenttools_copy_components_and_immediate_parent_of_first_component_05():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.BeamSpanner(staff[:4])
    u = componenttools.copy_components_and_immediate_parent_of_first_component(staff[0:1])

    beam_spanner = u[0]._get_spanner(spannertools.BeamSpanner)
    assert beam_spanner._is_my_only_leaf(u[0])


def test_componenttools_copy_components_and_immediate_parent_of_first_component_06():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.BeamSpanner(staff[:4])
    u = componenttools.copy_components_and_immediate_parent_of_first_component(
        staff[0:2])

    beam_spanner = u[0]._get_spanner(spannertools.BeamSpanner)
    assert beam_spanner._is_my_first_leaf(u[0])

    beam_spanner = u[1]._get_spanner(spannertools.BeamSpanner)
    assert beam_spanner._is_my_last_leaf(u[1])


def test_componenttools_copy_components_and_immediate_parent_of_first_component_07():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.BeamSpanner(staff[:4])
    u = componenttools.copy_components_and_immediate_parent_of_first_component(staff[0:4])

    beam_spanner = u[0]._get_spanner(spannertools.BeamSpanner)
    assert beam_spanner._is_my_first_leaf(u[0])

    assert u[1]._has_spanner(spannertools.BeamSpanner)
    assert u[2]._has_spanner(spannertools.BeamSpanner)
    
    beam_spanner = u[3]._get_spanner(spannertools.BeamSpanner)
    assert beam_spanner._is_my_last_leaf(u[3])
