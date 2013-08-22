# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_detach_spanners_attached_to_component_01():
    r'''Detach all spanners attached to component.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(container.select_leaves())
    slur = spannertools.SlurSpanner(container.select_leaves())
    trill = spannertools.TrillSpanner(container)

    spannertools.detach_spanners_attached_to_component(container[0])

    assert testtools.compare(
        container,
        r'''
        {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_spannertools_detach_spanners_attached_to_component_02():
    r'''Detach all spanners of class attached to component.
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
    spannertools.detach_spanners_attached_to_component(
        container[0], spanner_classes=spanner_classes)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 ( \startTrillSpan
            d'8
            e'8
            f'8 ) \stopTrillSpan
        }
        '''
        )

    assert inspect(container).is_well_formed()
