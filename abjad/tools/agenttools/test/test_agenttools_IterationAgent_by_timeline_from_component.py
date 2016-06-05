# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_timeline_from_component_01():
    r'''Yields component class instances in score of expr,
    sorted backward by score offset stop time,
    and starting from expr.
    '''

    score = Score()
    staff_1 = Staff("c'4 d'4 e'4 f'4")
    staff_2 = Staff("g'8 a'8 b'8 c''8")
    score.extend([staff_1, staff_2])

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        >>
        '''
        )

    leaf_generator = iterate(staff_2[2]).by_timeline_from_component(
        reverse=True,
        )
    leaves = list(leaf_generator)

    assert leaves[0] is staff_2[2] # b'8
    assert leaves[1] is staff_1[0] # c'4
    assert leaves[2] is staff_2[1] # a'8
    assert leaves[3] is staff_2[0] # g'8


def test_agenttools_IterationAgent_by_timeline_from_component_02():
    r'''Yields component class instances in score of expr,
    sorted backward by score offset stop time,
    and starting from expr.
    '''

    score = Score()
    staff_1 = Staff("c'8 d'8 e'8 f'8")
    staff_2 = Staff("g'4 a'4 b'4 c''4")
    score.extend([staff_1, staff_2])

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                g'4
                a'4
                b'4
                c''4
            }
        >>
        '''
        )

    leaf_generator = iterate(staff_1[3]).by_timeline_from_component(
        reverse=True,
        )
    leaves = list(leaf_generator)

    assert leaves[0] is staff_1[3] # f'8
    assert leaves[1] is staff_2[1] # a'4
    assert leaves[2] is staff_1[2] # e'8
    assert leaves[3] is staff_1[1] # d'8
    assert leaves[4] is staff_2[0] # g'4
    assert leaves[5] is staff_1[0] # c'8


def test_agenttools_IterationAgent_by_timeline_from_component_03():
    r'''Yields component class instances in score of expr,
    sorted by score offset and score index,
    and starting from expr.
    '''

    score = Score()
    staff_1 = Staff("c'4 d'4 e'4 f'4")
    staff_2 = Staff("g'8 a'8 b'8 c''8")
    score.extend([staff_1, staff_2])

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        >>
        '''
        )

    leaf_generator = iterate(staff_2[2]).by_timeline_from_component()
    leaves = list(leaf_generator)

    assert leaves[0] is staff_2[2] # b'8
    assert leaves[1] is staff_2[3] # c''8
    assert leaves[2] is staff_1[2] # e'4
    assert leaves[3] is staff_1[3] # f'4


def test_agenttools_IterationAgent_by_timeline_from_component_04():
    r'''Yields component class instances in score of expr,
    sorted by score offset and score index,
    and starting from expr.
    '''

    score = Score()
    staff_1 = Staff("c'8 d'8 e'8 f'8")
    staff_2 = Staff("g'4 a'4 b'4 c''4")
    score.extend([staff_1, staff_2])

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                g'4
                a'4
                b'4
                c''4
            }
        >>
        '''
        )

    leaf_generator = iterate(staff_1[3]).by_timeline_from_component()
    leaves = list(leaf_generator)

    assert leaves[0] is staff_1[3] # f'8
    assert leaves[1] is staff_2[2] # b'4
    assert leaves[2] is staff_2[3] # c''4
