# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_get_measure_01():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert scoretools.get_measure(staff, 1) is \
        staff[0]
    assert scoretools.get_measure(staff, 2) is \
        staff[1]
    assert scoretools.get_measure(staff, 3) is \
        staff[2]


def test_scoretools_get_measure_02():

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    assert pytest.raises(
        ValueError,
        'scoretools.get_measure(staff, -1)',
        )
