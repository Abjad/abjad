# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_MultipartBeam___format___01():

    container = Container("c'8 d'8 r8 e'8 f'8 g'4")
    beam = spannertools.MultipartBeam()
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
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


def test_spannertools_MultipartBeam___format___02():

    container = Container("c'8 r4 c'8")
    beam = spannertools.MultipartBeam()
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8
            r4
            c'8
        }
        '''
        )


def test_spannertools_MultipartBeam___format___03():

    container = Container("c'8. r16 c'8. r16")
    beam = spannertools.MultipartBeam()
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8.
            r16
            c'8.
            r16
        }
        '''
        )