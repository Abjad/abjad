# -*- encoding: utf-8 -*-
from abjad import *


def test_Measure_special_prolation_01():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    t = Measure((4, 4), Note("c'4") * 4)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].duration == Duration(1, 4)


def test_Measure_special_prolation_02():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    t = Measure((4, 4), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4")])
    assert t.select_leaves()[0].written_duration == Duration(1, 4)
    assert t.select_leaves()[0].duration == Duration(1, 4)
    assert t.select_leaves()[1].written_duration == Duration(1, 4)
    assert t.select_leaves()[1].duration == Duration(1, 6)


def test_Measure_special_prolation_03():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    t = Measure((4, 4), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), [
            tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4")])
    assert t.select_leaves()[0].written_duration == Duration(1, 4)
    assert t.select_leaves()[0].duration == Duration(1, 4)
    assert t.select_leaves()[1].written_duration == Duration(1, 4)
    assert t.select_leaves()[1].duration == Duration(1, 9)


def test_Measure_special_prolation_04():
    r'''Measures without power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    t = Measure((4, 5), Note("c'4") * 4)
    assert t[0].written_duration == Duration(1, 4)
    assert t[0].duration == Duration(1, 5)


def test_Measure_special_prolation_05():
    r'''Measures without power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    t = Measure((4, 5), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4")])
    assert t.select_leaves()[0].written_duration == Duration(1, 4)
    assert t.select_leaves()[0].duration == Duration(1, 5)
    assert t.select_leaves()[1].written_duration == Duration(1, 4)
    assert t.select_leaves()[1].duration == Duration(2, 15)


def test_Measure_special_prolation_06():
    r'''Measures without power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    t = Measure((4, 5), [
        Note("c'4"),
        tuplettools.FixedDurationTuplet(Duration(2, 4), [
            tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4")])
    assert t.select_leaves()[0].written_duration == Duration(1, 4)
    assert t.select_leaves()[0].duration == Duration(1, 5)
    assert t.select_leaves()[1].written_duration == Duration(1, 4)
    assert t.select_leaves()[1].duration == Duration(4, 45)
