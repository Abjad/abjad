# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_get_next_measure_from_component_01():

    staff = Staff()
    staff.append(Container("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"))
    staff.extend("abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    e'8
                    f'8
                }
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    leaves = select(staff).by_leaf()
    assert scoretools.get_next_measure_from_component(staff) is staff[0][0]
    assert scoretools.get_next_measure_from_component(staff[0]) is staff[0][0]
    assert scoretools.get_next_measure_from_component(staff[0][0]) is staff[0][1]
    assert scoretools.get_next_measure_from_component(staff[0][1]) is staff[1]
    assert scoretools.get_next_measure_from_component(staff[1]) is staff[2]
    assert scoretools.get_next_measure_from_component(staff[2]) is None
    assert scoretools.get_next_measure_from_component(
        leaves[0]) is staff[0][0]
    assert scoretools.get_next_measure_from_component(
        leaves[1]) is staff[0][0]
    assert scoretools.get_next_measure_from_component(
        leaves[2]) is staff[0][1]
    assert scoretools.get_next_measure_from_component(
        leaves[3]) is staff[0][1]
    assert scoretools.get_next_measure_from_component(
        leaves[4]) is staff[1]
    assert scoretools.get_next_measure_from_component(
        leaves[5]) is staff[1]
    assert scoretools.get_next_measure_from_component(
        leaves[6]) is staff[2]
    assert scoretools.get_next_measure_from_component(
        leaves[7]) is staff[2]


def test_scoretools_get_next_measure_from_component_02():
    r'''Can retrieve first measure in a Python list.
    '''

    components = [Note("c'4"), Measure((2, 8), "c'8 d'8")]

    result = scoretools.get_next_measure_from_component(components)
    assert result is components[1]
