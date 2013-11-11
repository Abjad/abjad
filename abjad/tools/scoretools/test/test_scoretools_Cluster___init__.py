# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Cluster___init___01():
    r'''Cluster can be empty.
    '''
    cluster = scoretools.Cluster([])
    assert not cluster.is_simultaneous
    assert len(cluster) == 0
    assert systemtools.TestManager.compare(
        cluster,
        r'''
        \makeClusters {
        }
        '''
        )


def test_scoretools_Cluster___init___02():
    cluster = scoretools.Cluster(Note(1, (1, 4)) * 4)
    assert isinstance(cluster, scoretools.Cluster)
    assert not cluster.is_simultaneous
    assert len(cluster) == 4
    assert systemtools.TestManager.compare(
        cluster,
        r'''
        \makeClusters {
            cs'4
            cs'4
            cs'4
            cs'4
        }
        '''
        )
