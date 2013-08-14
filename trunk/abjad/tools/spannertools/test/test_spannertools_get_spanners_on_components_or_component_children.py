# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_get_spanners_on_components_or_component_children_01():
    r'''Get all spanners attaching directly to any component in list.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam_1 = spannertools.BeamSpanner(container[:2])
    beam_2 = spannertools.BeamSpanner(container[2:])
    crescendo = spannertools.CrescendoSpanner(container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ \<
            d'8 ]
            e'8 [
            f'8 ] \!
        }
        '''
        )

    spanners = spannertools.get_spanners_on_components_or_component_children(
        container[:])

    assert beam_1 in spanners
    assert beam_2 in spanners
    assert crescendo not in spanners


def test_spannertools_get_spanners_on_components_or_component_children_02():
    r'''Accept empty component list.
    '''

    spanners = spannertools.get_spanners_on_components_or_component_children(
        [])

    assert spanners == set([])


def test_spannertools_get_spanners_on_components_or_component_children_03():
    r'''Return empty set when no spanners.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    spanners = spannertools.get_spanners_on_components_or_component_children(
        container[:])

    assert spanners == set([])
