# -*- encoding: utf-8 -*-
from abjad import *


def test_BeamSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4], direction=Up)

    r'''
    \new Staff {
        c'8 ^ [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
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


def test_BeamSpanner_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4], direction=Down)

    r'''
    \new Staff {
        c'8 _ [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
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


def test_BeamSpanner_direction_03():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4], direction=Center)

    r'''
    \new Staff {
        c'8 - [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
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
