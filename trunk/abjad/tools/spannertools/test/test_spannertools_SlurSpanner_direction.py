# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_SlurSpanner_direction_01():

    container = Container("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(direction=Up)
    slur.attach(container)

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

    assert inspect(container).get_spanners() == set([slur])
