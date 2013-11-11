# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Slur_direction_01():

    container = Container("c'8 d'8 e'8 f'8")
    slur = Slur(direction=Up)
    attach(slur, container)

    assert systemtools.TestManager.compare(
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
