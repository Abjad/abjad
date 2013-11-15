# -*- encoding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_Container___copy___01():
    r'''Containers copy simultaneity flag.
    '''

    container_1 = Container([Voice("c'8 d'8"), Voice("c''8 b'8")])
    container_1.is_simultaneous = True
    container_2 = copy.copy(container_1)


    assert systemtools.TestManager.compare(
        container_1,
        r'''
        <<
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                c''8
                b'8
            }
        >>
        '''
        )

    assert systemtools.TestManager.compare(
        container_2,
        r'''
        <<
        >>
        '''
        )

    assert container_1 is not container_2
