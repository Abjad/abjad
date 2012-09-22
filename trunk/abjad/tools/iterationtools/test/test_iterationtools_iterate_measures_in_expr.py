from abjad import *


def test_iterationtools_iterate_measures_in_expr_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    measures = list(iterationtools.iterate_measures_in_expr(staff, reverse=True))

    assert measures[0] is staff[2]
    assert measures[1] is staff[1]
    assert measures[2] is staff[0]


def test_iterationtools_iterate_measures_in_expr_02():
    '''Optional start and stop keyword paramters.'''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    measures = list(iterationtools.iterate_measures_in_expr(staff, start=1, reverse=True))
    assert measures[0] is staff[1]
    assert measures[1] is staff[0]
    assert len(measures) == 2

    measures = list(iterationtools.iterate_measures_in_expr(staff, stop=2, reverse=True))
    assert measures[0] is staff[2]
    assert measures[1] is staff[1]
    assert len(measures) == 2


def test_iterationtools_iterate_measures_in_expr_03():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    measures = list(iterationtools.iterate_measures_in_expr(staff))

    assert measures[0] is staff[0]
    assert measures[1] is staff[1]
    assert measures[2] is staff[2]


def test_iterationtools_iterate_measures_in_expr_04():
    '''Optional start and stop keyword paramters.'''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    measures = list(iterationtools.iterate_measures_in_expr(staff, start=1))
    assert measures[0] is staff[1]
    assert measures[1] is staff[2]
    assert len(measures) == 2

    measures = list(iterationtools.iterate_measures_in_expr(staff, stop=2))
    assert measures[0] is staff[0]
    assert measures[1] is staff[1]
    assert len(measures) == 2
