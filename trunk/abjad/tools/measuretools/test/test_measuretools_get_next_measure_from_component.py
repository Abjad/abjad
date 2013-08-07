# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_measuretools_get_next_measure_from_component_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    Container(staff[:2])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        {
                \time 2/8
                c'8
                d'8
                \time 2/8
                e'8
                f'8
        }
            \time 2/8
            g'8
            a'8
            \time 2/8
            b'8
            c''8
    }
    '''

    assert measuretools.get_next_measure_from_component(staff) is staff[0][0]
    assert measuretools.get_next_measure_from_component(staff[0]) is staff[0][0]
    assert measuretools.get_next_measure_from_component(staff[0][0]) is staff[0][1]
    assert measuretools.get_next_measure_from_component(staff[0][1]) is staff[1]
    assert measuretools.get_next_measure_from_component(staff[1]) is staff[2]
    #assert py.test.raises(StopIteration, 'measuretools.get_next_measure_from_component(staff[2])')
    assert measuretools.get_next_measure_from_component(staff[2]) is None
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[0]) is staff[0][0]
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[1]) is staff[0][0]
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[2]) is staff[0][1]
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[3]) is staff[0][1]
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[4]) is staff[1]
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[5]) is staff[1]
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[6]) is staff[2]
    assert measuretools.get_next_measure_from_component(staff.select_leaves()[7]) is staff[2]


def test_measuretools_get_next_measure_from_component_02():
    r'''Can retrieve first measure in a Python list.
    '''

    t = [Note("c'4"), Measure((2, 8), "c'8 d'8")]

    assert measuretools.get_next_measure_from_component(t) is t[1]
