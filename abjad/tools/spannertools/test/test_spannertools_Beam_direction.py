# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Beam_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beam = Beam(direction=Up)
    attach(beam, staff[:4])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 ^ [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )


def test_spannertools_Beam_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beam = Beam(direction=Down)
    attach(beam, staff[:4])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 _ [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )


def test_spannertools_Beam_direction_03():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beam = Beam(direction=Center)
    attach(beam, staff[:4])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 - [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )
