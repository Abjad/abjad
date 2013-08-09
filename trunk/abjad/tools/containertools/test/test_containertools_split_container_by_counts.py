# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_split_container_by_counts_01():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    containertools.split_container_by_counts(voice[0], [1, 3], cyclic=True, fracture_spanners=False)

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


    assert select(voice).is_well_formed()
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


def test_containertools_split_container_by_counts_02():
    r'''Cyclic by [1] splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    containertools.split_container_by_counts(voice[0], [1], cyclic=True, fracture_spanners=False)

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

    assert select(voice).is_well_formed()
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


def test_containertools_split_container_by_counts_03():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [1, 3], cyclic=True, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 4
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


def test_containertools_split_container_by_counts_04():
    r'''Cyclic by [1] splits all elements in container.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [1], cyclic=True, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 4
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


def test_containertools_split_container_by_counts_05():
    r'''Partition by large part count.
        Input container cedes contents to new instance.
        Expression appears unaltered.'''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())
    container = voice[0]

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

    parts = containertools.split_container_by_counts(voice[0], [100], cyclic=True, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 1
    assert container is not voice[0]
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


def test_containertools_split_container_by_counts_06():
    r'''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [2, 2, 2, 2, 2], cyclic=True, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 2
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


def test_containertools_split_container_by_counts_07():
    r'''Partition by large empty part counts list.
    Empty list returns and expression remains unaltered.
    '''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [], cyclic=True, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 1
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


def test_containertools_split_container_by_counts_08():
    r'''Partition container into parts of lengths equal to counts.
        Read list of counts only once; do not cycle.
        Fracture spanners attaching directly to container.
        Leave spanner attaching to container contents untouched.'''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [1, 3], cyclic=False, fracture_spanners=False)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 3
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


def test_containertools_split_container_by_counts_09():
    r'''Partition container into parts of lengths equal to counts.
    Read list of counts only once; do not cycle.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.'''

    voice = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [1, 3], cyclic=False, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 3
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


def test_containertools_split_container_by_counts_10():
    r'''Partition by large part count.
    Input container cedes contents to new instance.
    Expression appears unaltered.'''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())
    container = voice[0]

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

    parts = containertools.split_container_by_counts(voice[0], [100], cyclic=False, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 1
    assert container is not voice[0]
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


def test_containertools_split_container_by_counts_11():
    r'''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.'''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [2, 2, 2, 2, 2], cyclic=False, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 2
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


def test_containertools_split_container_by_counts_12():
    r'''Partition by empty part counts list.
    Input container returns within one-element result list.'''

    voice = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(voice[0])
    spannertools.SlurSpanner(voice[0].select_leaves())

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

    parts = containertools.split_container_by_counts(voice[0], [], cyclic=False, fracture_spanners=True)

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

    assert select(voice).is_well_formed()
    assert len(parts) == 1
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
