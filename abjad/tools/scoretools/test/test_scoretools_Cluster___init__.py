# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Cluster___init___01():
    r'''Cluster can be empty.
    '''
    cluster = abjad.Cluster([])
    assert not cluster.is_simultaneous
    assert len(cluster) == 0
    assert format(cluster) == abjad.String.normalize(
        r'''
        \makeClusters {
        }
        '''
        )


def test_scoretools_Cluster___init___02():
    cluster = abjad.Cluster(abjad.Note(1, (1, 4)) * 4)
    assert isinstance(cluster, abjad.Cluster)
    assert not cluster.is_simultaneous
    assert len(cluster) == 4
    assert format(cluster) == abjad.String.normalize(
        r'''
        \makeClusters {
            cs'4
            cs'4
            cs'4
            cs'4
        }
        '''
        )
