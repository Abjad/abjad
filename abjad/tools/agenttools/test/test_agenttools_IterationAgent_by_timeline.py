# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_timeline_01():
    r'''Yields component class instances in expr sorted backward
    by score offset stop time.
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

    leaf_generator = iterate(score).by_timeline(reverse=True)
    leaves = list(leaf_generator)

    assert leaves[0] is staff_1[3] # f'4
    assert leaves[1] is staff_1[2] # e'4
    assert leaves[2] is staff_1[1] # d'4
    assert leaves[3] is staff_2[3] # c''8
    assert leaves[4] is staff_2[2] # b'8
    assert leaves[5] is staff_1[0] # c'4
    assert leaves[6] is staff_2[1] # a'8
    assert leaves[7] is staff_2[0] # g'8


def test_agenttools_IterationAgent_by_timeline_02():
    r'''Yields component class instances in expr sorted by score offset
    and score index.
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

    leaf_generator = iterate(score).by_timeline(reverse=True)
    leaves = list(leaf_generator)

    assert leaves[0] is staff_2[3] # c''4
    assert leaves[1] is staff_2[2] # b'4
    assert leaves[2] is staff_1[3] # f'8
    assert leaves[3] is staff_2[1] # a'4
    assert leaves[4] is staff_1[2] # e'8
    assert leaves[5] is staff_1[1] # d'8
    assert leaves[6] is staff_2[0] # g'4
    assert leaves[7] is staff_1[0] # c'8


def test_agenttools_IterationAgent_by_timeline_03():
    r'''Yields component class instances in expr sorted by score offset
    and score index.
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

    leaf_generator = iterate(score).by_timeline()
    leaves = list(leaf_generator)

    assert leaves[0] is staff_1[0] # c'4
    assert leaves[1] is staff_2[0] # g'8
    assert leaves[2] is staff_2[1] # a'8
    assert leaves[3] is staff_1[1] # d'4
    assert leaves[4] is staff_2[2] # b'8
    assert leaves[5] is staff_2[3] # c''8
    assert leaves[6] is staff_1[2] # e'4
    assert leaves[7] is staff_1[3] # f'4


def test_agenttools_IterationAgent_by_timeline_04():
    r'''Yields component class instances in expr sorted by score offset
    and score index.
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

    leaf_generator = iterate(score).by_timeline()
    leaves = list(leaf_generator)

    assert leaves[0] is staff_1[0] # c'8
    assert leaves[1] is staff_2[0] # g'4
    assert leaves[2] is staff_1[1] # d'8
    assert leaves[3] is staff_1[2] # e'8
    assert leaves[4] is staff_2[1] # a'4
    assert leaves[5] is staff_1[3] # f'8
    assert leaves[6] is staff_2[2] # b'4
    assert leaves[7] is staff_2[3] # c''4


def test_agenttools_IterationAgent_by_timeline_05():

    staff_one = Staff(r"c'4 \times 2/3 { d'8 e' f' } g'2")
    staff_two = Staff('r2 fs2')
    staff_group = StaffGroup([staff_one, staff_two])
    score = Score([staff_group])

    component_generator = iterate(score).by_timeline(scoretools.Component)
    components = tuple(component_generator)

    assert components[0] is score
    assert components[1] is staff_group
    assert components[2] is staff_one
    assert components[3] is staff_one[0]
    assert components[4] is staff_two
    assert components[5] is staff_two[0]
    assert components[6] is staff_one[1]
    assert components[7] is staff_one[1][0]
    assert components[8] is staff_one[1][1]
    assert components[9] is staff_one[1][2]
    assert components[10] is staff_one[2]
    assert components[11] is staff_two[1]


def test_agenttools_IterationAgent_by_timeline_06():

    staff_one = Staff(r"c'4 \times 2/3 { d'8 e' f' } g'2")
    staff_two = Staff('r2 fs2')
    staff_group = StaffGroup([staff_one, staff_two])
    score = Score([staff_group])

    component_generator = iterate(score).by_timeline(
        scoretools.Component,
        reverse=True,
        )
    components = tuple(component_generator)

    assert components[0] is score
    assert components[1] is staff_group
    assert components[2] is staff_one
    assert components[3] is staff_one[2]
    assert components[4] is staff_two
    assert components[5] is staff_two[1]
    assert components[6] is staff_one[1]
    assert components[7] is staff_one[1][2]
    assert components[8] is staff_two[0]
    assert components[9] is staff_one[1][1]
    assert components[10] is staff_one[1][0]
    assert components[11] is staff_one[0]


def test_agenttools_IterationAgent_by_timeline_07():

    staff_one = Staff(r"c'4 << \times 2/3 { d' e' f' } { b' a' } >> g'4")
    staff_two = Staff("c,2 e,2")
    staff_group = StaffGroup([staff_one, staff_two])
    score = Score([staff_group])

    component_generator = iterate(score).by_timeline(
        scoretools.Component,
        )
    components = tuple(component_generator)

    assert components[0] is score
    assert components[1] is staff_group
    assert components[2] is staff_one
    assert components[3] is staff_one[0]
    assert components[4] is staff_two
    assert components[5] is staff_two[0]
    assert components[6] is staff_one[1]
    assert components[7] is staff_one[1][0]
    assert components[8] is staff_one[1][0][0]
    assert components[9] is staff_one[1][1]
    assert components[10] is staff_one[1][1][0]
    assert components[11] is staff_one[1][0][1]
    assert components[12] is staff_one[1][1][1]
    assert components[13] is staff_two[1]
    assert components[14] is staff_one[1][0][2]
    assert components[15] is staff_one[2]


def test_agenttools_IterationAgent_by_timeline_08():

    staff_one = Staff(r"c'4 << \times 2/3 { d' e' f' } { b' a' } >> g'4")
    staff_two = Staff("c,2 e,2")
    staff_group = StaffGroup([staff_one, staff_two])
    score = Score([staff_group])

    component_generator = iterate(score).by_timeline(
        scoretools.Component,
        reverse=True
        )
    components = tuple(component_generator)

    assert components[0] is score
    assert components[1] is staff_group
    assert components[2] is staff_one
    assert components[3] is staff_one[2]
    assert components[4] is staff_two
    assert components[5] is staff_two[1]
    assert components[6] is staff_one[1]
    assert components[7] is staff_one[1][0]
    assert components[8] is staff_one[1][0][2]
    assert components[9] is staff_one[1][1]
    assert components[10] is staff_one[1][1][1]
    assert components[11] is staff_one[1][0][1]
    assert components[12] is staff_one[1][1][0]
    assert components[13] is staff_two[0]
    assert components[14] is staff_one[1][0][0]
    assert components[15] is staff_one[0]
