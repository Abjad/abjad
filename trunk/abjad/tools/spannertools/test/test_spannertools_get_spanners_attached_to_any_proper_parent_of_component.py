# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_get_spanners_attached_to_any_proper_parent_of_component_01():

    container = Container("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(container.select_leaves())
    slur = spannertools.SlurSpanner(container.select_leaves())
    trill = spannertools.TrillSpanner(container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }
        '''
        )

    assert spannertools.get_spanners_attached_to_any_proper_parent_of_component(
        container[0]) == set([trill])
    assert spannertools.get_spanners_attached_to_any_proper_parent_of_component(
        container) == set([])
