# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_measuretools_get_previous_measure_from_component_01():

    staff = Staff()
    staff.append(Container("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"))
    staff.extend("abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert testtools.compare(
        staff,
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

    assert measuretools.get_previous_measure_from_component(staff) is staff[-1]
    assert measuretools.get_previous_measure_from_component(staff[0]) is staff[0][1]
    assert measuretools.get_previous_measure_from_component(staff[0][0]) is None
    assert measuretools.get_previous_measure_from_component(staff[0][1]) is staff[0][0]
    assert measuretools.get_previous_measure_from_component(staff[1]) is staff[0][1]
    assert measuretools.get_previous_measure_from_component(staff[2]) is staff[1]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[0]) is staff[0][0]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[1]) is staff[0][0]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[2]) is staff[0][1]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[3]) is staff[0][1]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[4]) is staff[1]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[5]) is staff[1]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[6]) is staff[2]
    assert measuretools.get_previous_measure_from_component(
        staff.select_leaves()[7]) is staff[2]


def test_measuretools_get_previous_measure_from_component_02():
    r'''Can retrieve last measure in a Python list.
    '''

    components = [Measure((2, 8), "c'8 d'8"), Note("c'4")]

    result = measuretools.get_previous_measure_from_component(components) 
    assert result is components[0]
