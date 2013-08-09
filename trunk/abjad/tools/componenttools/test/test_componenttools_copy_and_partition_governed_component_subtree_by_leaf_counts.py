# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_copy_and_partition_governed_component_subtree_by_leaf_counts_01():
    r'''Partition tuplet in voice.
    The helper wraps lcopy().
    This means that the original structure remains unchanged.
    Also that resulting parts cut all the way up into voice.
    '''

    voice = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    spannertools.BeamSpanner(voice[0][:])
    left, right = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(voice[0], [1, 2])

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [ ]
        }
    }
    '''

    assert select(left).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [ ]
            }
        }
        '''
        )

    r'''
    \new Voice {
        \times 2/3 {
            d'8 [
            e'8 ]
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        right,
        r'''
        \new Voice {
            \times 2/3 {
                d'8 [
                e'8 ]
            }
        }
        '''
        )


def test_componenttools_copy_and_partition_governed_component_subtree_by_leaf_counts_02():
    r'''Partition voice.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    result = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(voice, [1, 2])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    r'''
    \new Voice {
        c'8 [ ]
    }
    '''

    assert select(result[0]).is_well_formed()
    assert testtools.compare(
        result[0],
        r'''
        \new Voice {
            c'8 [ ]
        }
        '''
        )

    r'''
    \new Voice {
        d'8 [
        e'8 ]
    }
    '''

    assert select(result[-1]).is_well_formed()
    assert testtools.compare(
        result[-1],
        r'''
        \new Voice {
            d'8 [
            e'8 ]
        }
        '''
        )
