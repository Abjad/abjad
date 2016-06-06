# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Tuplet_from_duration_and_ratio_01():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'32
            c'32
            c'32
            c'32
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'32
            c'32
            c'32
            c'32
            c'32
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_02():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'32
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'64
            c'32
            c'32
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 12/11 {
            c'64
            c'32
            c'32
            c'32.
            c'32.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_03():
    r'''Interpret negative proportions as rests.
    '''

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 12/11 {
            c'64
            r32
            r32
            c'32.
            c'32.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_04():
    r'''Reduce proportions relative to each other.
    '''

    duration = Duration(3, 16)

    tuplet_1 = Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    tuplet_2 = Tuplet.from_duration_and_ratio(
        duration,
        [2, -4, -4, 6, 6],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = Tuplet.from_duration_and_ratio(
        Duration(1, 8),
        [27],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_05():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 8/5 {
            c'64.
            c'64.
            c'64.
            c'64.
            c'64.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_06():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 8/5 {
            c'64.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'64
            c'32
            c'32
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 12/11 {
            c'64
            c'32
            c'32
            c'32.
            c'32.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_07():
    r'''Reduce proportions relative to each other.
    '''

    duration = Duration(3, 16)

    tuplet_1 = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=False,
        is_diminution=False,
        )

    tuplet_2 = Tuplet.from_duration_and_ratio(
        duration,
        [2, 4, 4, 6, 6],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = Tuplet.from_duration_and_ratio(
        Duration(1, 8),
        [27], avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_08():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'4
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'8
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'16
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'16
            c'16
            c'16
            c'16
            c'16
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_09():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'4
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'16
            c'8
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'32
            c'16
            c'16
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/11 {
            c'32
            c'16
            c'16
            c'16.
            c'16.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_10():
    r'''Interpret negative proportions as rests.
    '''

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/11 {
            c'32
            r16
            r16
            c'16.
            c'16.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_11():
    r'''Reduce propotions relative to each other.
    '''

    duration = Duration(3, 16)

    tuplet_1 = Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    tuplet_2 = Tuplet.from_duration_and_ratio(
        duration,
        [2, -4, -4, 6, 6],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = Tuplet.from_duration_and_ratio(Duration(1, 8), [27])

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_12():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 4/5 {
            c'32.
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_13():

    duration = Duration(3, 16)

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 4/5 {
            c'32.
            c'16.
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'32
            c'16
            c'16
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/11 {
            c'32
            c'16
            c'16
            c'16.
            c'16.
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_14():
    r'''Reduce proportions relative to each other.
    '''

    duration = Duration(3, 16)

    tuplet_1 = Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=False,
        is_diminution=True,
        )

    tuplet_2 = Tuplet.from_duration_and_ratio(
        duration,
        [2, -4, -4, 6, 6],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = Tuplet.from_duration_and_ratio(
        Duration(1, 8),
        [27],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_15():
    r'''Coerce duration.
    '''

    tuplet = Tuplet.from_duration_and_ratio(
        Duration(1, 4),
        [1, -1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 2/3 {
            c'8
            r8
            c'8
        }
        '''
        )
