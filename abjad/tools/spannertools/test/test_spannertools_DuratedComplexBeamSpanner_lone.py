# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeamSpanner_lone_01():
    r'''Span lone note when lone is set to true.
    '''

    container = Container("c'8")
    beam = spannertools.DuratedComplexBeamSpanner(lone=True)
    attach(beam, container)

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            c'8 [ ]
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_spannertools_DuratedComplexBeamSpanner_lone_02():
    r'''Do not span lone note when lone is set to false.
    '''

    container = Container("c'8")
    beam = spannertools.DuratedComplexBeamSpanner(lone=False)
    attach(beam, container)

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_spannertools_DuratedComplexBeamSpanner_lone_03():
    r'''Ignore lone when spanner spans more than one leaf.
    '''

    container = Container("c'8 d'8")
    beam = spannertools.DuratedComplexBeamSpanner(lone=False)
    attach(beam, container)

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #1
            c'8 [
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #0
            d'8 ]
        }
        '''
        )

    assert inspect(container).is_well_formed()
