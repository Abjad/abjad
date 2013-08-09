# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_Container___copy___01():
    r'''Containes copy simultaneous indicator.
    '''

    container_1 = Container([Voice("c'8 d'8"), Voice("c''8 b'8")])
    container_1.is_simultaneous = True

    container_2 = copy.copy(container_1)


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

    assert container_1 is not container_2
    assert testtools.compare(
        container_2,
        r'''
        <<
        >>
        '''
        )
