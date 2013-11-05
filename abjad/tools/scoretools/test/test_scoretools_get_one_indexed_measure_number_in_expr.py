# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_scoretools_get_one_indexed_measure_number_in_expr_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert scoretools.get_one_indexed_measure_number_in_expr(staff, 1) is \
        staff[0]
    assert scoretools.get_one_indexed_measure_number_in_expr(staff, 2) is \
        staff[1]
    assert scoretools.get_one_indexed_measure_number_in_expr(staff, 3) is \
        staff[2]


def test_scoretools_get_one_indexed_measure_number_in_expr_02():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert py.test.raises(
        ValueError, 
        'scoretools.get_one_indexed_measure_number_in_expr(staff, -1)',
        )
