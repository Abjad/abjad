# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_fracture_spanners_attached_to_component_01():

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

    spannertools.fracture_spanners_attached_to_component(
    container[1], direction=Right)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ ( \startTrillSpan
            d'8 ] )
            e'8 [ (
            f'8 ] ) \stopTrillSpan
        }
        '''
        )

    assert select(container).is_well_formed()


def test_spannertools_fracture_spanners_attached_to_component_02():
    r'''With spanner classes filter.
    '''

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

    spanner_classes = (spannertools.BeamSpanner, )
    spannertools.fracture_spanners_attached_to_component(
        container[1], direction=Right, spanner_classes=spanner_classes)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ ( \startTrillSpan
            d'8 ]
            e'8 [
            f'8 ] ) \stopTrillSpan
        }
        '''
        )

    assert select(container).is_well_formed()
