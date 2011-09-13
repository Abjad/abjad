from abjad import *


def test_spannertools_get_spanners_on_components_or_component_children_01():
    '''Get all spanners attaching directly to any component in list.'''

    t = Staff("c'8 d'8 e'8 f'8")
    b1 = spannertools.BeamSpanner(t[:2])
    b2 = spannertools.BeamSpanner(t[2:])
    crescendo = spannertools.CrescendoSpanner(t)

    r'''
    \new Staff {
        c'8 [ \<
        d'8 ]
        e'8 [
        f'8 ] \!
    }
    '''

    spanners = spannertools.get_spanners_on_components_or_component_children(t[:])

    assert b1 in spanners
    assert b2 in spanners
    assert crescendo not in spanners


def test_spannertools_get_spanners_on_components_or_component_children_02():
    '''Accept empty component list.'''

    spanners = spannertools.get_spanners_on_components_or_component_children([])

    assert spanners == set([])


def test_spannertools_get_spanners_on_components_or_component_children_03():
    '''Return empty set when no spanners.'''

    t = Staff("c'8 d'8 e'8 f'8")
    spanners = spannertools.get_spanners_on_components_or_component_children(t[:])

    assert spanners == set([])
