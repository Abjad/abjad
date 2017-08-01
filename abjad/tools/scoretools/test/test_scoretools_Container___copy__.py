# -*- coding: utf-8 -*-
import abjad
import copy


def test_scoretools_Container___copy___01():
    r'''Containers copy simultaneity flag.
    '''

    container_1 = abjad.Container([abjad.Voice("c'8 d'8"), abjad.Voice("c''8 b'8")])
    container_1.is_simultaneous = True
    container_2 = copy.copy(container_1)


    assert format(container_1) == abjad.String.normalize(
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

    assert format(container_2) == abjad.String.normalize(
        r'''
        <<
        >>
        '''
        )

    assert container_1 is not container_2
