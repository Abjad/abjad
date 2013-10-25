# -*- encoding: utf-8 -*-
from abjad import *


def test_MultipartBeamSpanner_format_01():

    container = Container("c'8 d'8 r8 e'8 f'8 g'4")
    beam = spannertools.MultipartBeamSpanner()
    beam.attach(container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [
            d'8 ]
            r8
            e'8 [
            f'8 ]
            g'4
        }
        '''
        )
