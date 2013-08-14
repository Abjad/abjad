# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner_direction_01():

    container = Container("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(container, direction=Up)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 ^ (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert more(container).get_spanners() == set([slur])
