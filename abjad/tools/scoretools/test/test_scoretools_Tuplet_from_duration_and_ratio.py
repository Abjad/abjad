# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Tuplet_from_duration_and_ratio_01():

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'32
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet_1 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=False,
        )

    tuplet_2 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [2, -4, -4, 6, 6],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        abjad.Duration(1, 8),
        [27],
        avoid_dots=True,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_05():

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 8/5 {
            c'64.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet_1 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=False,
        is_diminution=False,
        )

    tuplet_2 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [2, 4, 4, 6, 6],
        avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        abjad.Duration(1, 8),
        [27], avoid_dots=False,
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_08():

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'4
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'8
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'4
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'16
            c'8
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet_1 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=True,
        is_diminution=True,
        )

    tuplet_2 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [2, -4, -4, 6, 6],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = abjad.Tuplet.from_duration_and_ratio(abjad.Duration(1, 8), [27])

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_12():

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 1, 1, 1, 1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 4/5 {
            c'32.
            c'16.
            c'16.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, 2, 2, 3, 3],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
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

    duration = abjad.Duration(3, 16)

    tuplet_1 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [1, -2, -2, 3, 3],
        avoid_dots=False,
        is_diminution=True,
        )

    tuplet_2 = abjad.Tuplet.from_duration_and_ratio(
        duration,
        [2, -4, -4, 6, 6],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet_1) == format(tuplet_2)

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        abjad.Duration(1, 8),
        [27],
        avoid_dots=False,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_duration_and_ratio_15():
    r'''Coerce duration.
    '''

    tuplet = abjad.Tuplet.from_duration_and_ratio(
        abjad.Duration(1, 4),
        [1, -1, 1],
        avoid_dots=True,
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'8
            r8
            c'8
        }
        '''
        )
