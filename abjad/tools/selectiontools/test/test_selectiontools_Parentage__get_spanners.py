# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Parentage__get_spanners_01():
    '''Get spanners in proper parentage.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(Beam(), container[:])
    slur = Slur()
    attach(slur, container[:])
    trill = spannertools.TrillSpanner()
    attach(trill, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }
        '''
        )

    spanners = container[0]._get_parentage()._get_spanners()
    spanners == set([beam, slur, trill])
    spanners = container._get_parentage()._get_spanners()
    spanners == set([trill])


def test_selectiontools_Parentage__get_spanners_02():
    '''Get spanners in improper parentage.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, container[:])
    slur = Slur()
    attach(slur, container[:])
    trill = spannertools.TrillSpanner()
    attach(trill, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }
        '''
        )

    parentage = container._get_parentage(include_self=False)
    assert parentage._get_spanners() == set([])