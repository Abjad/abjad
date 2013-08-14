# -*- encoding: utf-8 -*-
from abjad import *


def test_MultipartBeamSpanner_direction_01():

    container = Container("c'8 d'8 r8 e'8 f'8 g'4")
    spanner = spannertools.MultipartBeamSpanner(container, direction=Up)

    assert testtools.compare(
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

    assert testtools.compare(
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
