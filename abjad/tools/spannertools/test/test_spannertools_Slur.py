# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Slur_01():
    r'''Slur spanner can attach to a container.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, container)

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert inspect(container).get_spanners() == set([slur])


def test_spannertools_Slur_02():
    r'''Slur spanner can attach to leaves.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, container[:])

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert len(inspect(container).get_spanners()) == 0
    for leaf in container.select_leaves():
        assert inspect(leaf).get_spanners() == set([slur])
