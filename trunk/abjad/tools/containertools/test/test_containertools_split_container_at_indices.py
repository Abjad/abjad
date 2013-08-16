# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_split_container_at_indices_01():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    containertools.split_container_at_indices(
        voice[0], 
        [1, 3], 
        cyclic=True, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
            }
            {
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()


def test_containertools_split_container_at_indices_02():
    r'''Cyclic 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    containertools.split_container_at_indices(
        voice[0], 
        [1], 
        cyclic=True, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
            }
            {
                e'8
            }
            {
                f'8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()


def test_containertools_split_container_at_indices_03():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [1, 3], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] (
            }
            {
                d'8 [
                e'8
                f'8 ]
            }
            {
                g'8 [ ]
            }
            {
                a'8 [
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 4


def test_containertools_split_container_at_indices_04():
    r'''Cyclic by 1 splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [1], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] (
            }
            {
                d'8 [ ]
            }
            {
                e'8 [ ]
            }
            {
                f'8 [ ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 4


def test_containertools_split_container_at_indices_05():
    r'''Split by large count. Container remains unchanged.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())
    container = voice[0]

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [100], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 1


def test_containertools_split_container_at_indices_06():
    r'''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [2, 2, 2, 2, 2], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 2


def test_containertools_split_container_at_indices_07():
    r'''Partition by large empty part counts list.
    Empty list returns and expression remains unaltered.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [], 
        cyclic=True, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 1


def test_containertools_split_container_at_indices_08():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts only once; do not cycle.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [1, 3], 
        cyclic=False, 
        fracture_spanners=False,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 3


def test_containertools_split_container_at_indices_09():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts only once; do not cycle.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [1, 3], 
        cyclic=False, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ ] (
            }
            {
                d'8 [
                e'8
                f'8 ]
            }
            {
                g'8 [
                a'8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 3


def test_containertools_split_container_at_indices_10():
    r'''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [2, 2, 2, 2, 2], 
        cyclic=False, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 2


def test_containertools_split_container_at_indices_11():
    r'''Partition by empty part counts list.
    Input container returns within one-element result list.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    parts = containertools.split_container_at_indices(
        voice[0], 
        [], 
        cyclic=False, 
        fracture_spanners=True,
        )

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8 ] )
            }
        }
        '''
        )

    assert select(voice).is_well_formed()
    assert len(parts) == 1
