# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_MultipartBeamSpanner_direction_01():

    container = Container("c'8 d'8 r8 e'8 f'8 g'4")
    spanner = spannertools.MultipartBeamSpanner(direction=Up)
    attach(spanner, container)

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8 ^ [
            d'8 ]
            r8
            e'8 ^ [
            f'8 ]
            g'4
        }
        '''
        )

    spanner.direction = Down

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8 _ [
            d'8 ]
            r8
            e'8 _ [
            f'8 ]
            g'4
        }
        '''
        )
