# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_MultipartBeam_direction_01():

    container = Container("c'8 d'8 r8 e'8 f'8 g'4")
    beam = spannertools.MultipartBeam(direction=Up)
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
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

    detach(beam, container[:])
    beam = spannertools.MultipartBeam(direction=Down)
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
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