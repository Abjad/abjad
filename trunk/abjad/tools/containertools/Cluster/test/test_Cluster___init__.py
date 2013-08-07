# -*- encoding: utf-8 -*-
from abjad import *


def test_Cluster___init___01():
    r'''Cluster can be empty.
    '''
    cluster = containertools.Cluster([])
    assert not cluster.is_parallel
    assert len(cluster) == 0
    assert testtools.compare(
        cluster.lilypond_format,
        r'''
        \makeClusters {
        }
        '''
        )


def test_Cluster___init___02():
    cluster = containertools.Cluster(Note(1, (1, 4)) * 4)
    assert isinstance(cluster, containertools.Cluster)
    assert not cluster.is_parallel
    assert len(cluster) == 4
    assert testtools.compare(
        cluster.lilypond_format,
        r'''
        \makeClusters {
            cs'4
            cs'4
            cs'4
            cs'4
        }
        '''
        )
