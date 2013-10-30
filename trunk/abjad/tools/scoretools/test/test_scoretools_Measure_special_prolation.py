# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_special_prolation_01():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    measure = Measure((4, 4), Note("c'4") * 4)
    assert measure[0].written_duration == Duration(1, 4)
    assert inspect(measure[0]).get_duration() == Duration(1, 4)


def test_scoretools_Measure_special_prolation_02():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    measure = Measure((4, 4), [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4")])
    assert measure.select_leaves()[0].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[0]).get_duration() == Duration(1, 4)
    assert measure.select_leaves()[1].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[1]).get_duration() == Duration(1, 6)


def test_scoretools_Measure_special_prolation_03():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    measure = Measure((4, 4), [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), [
            scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4")])
    assert measure.select_leaves()[0].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[0]).get_duration() == Duration(1, 4)
    assert measure.select_leaves()[1].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[1]).get_duration() == Duration(1, 9)


def test_scoretools_Measure_special_prolation_04():
    r'''Measures without power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    measure = Measure((4, 5), Note("c'4") * 4)
    assert measure[0].written_duration == Duration(1, 4)
    assert inspect(measure[0]).get_duration() == Duration(1, 5)


def test_scoretools_Measure_special_prolation_05():
    r'''Measures without power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    measure = Measure((4, 5), [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4")])
    assert measure.select_leaves()[0].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[0]).get_duration() == Duration(1, 5)
    assert measure.select_leaves()[1].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[1]).get_duration() == Duration(2, 15)


def test_scoretools_Measure_special_prolation_06():
    r'''Measures without power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    measure = Measure((4, 5), [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), [
            scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4")])
    assert measure.select_leaves()[0].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[0]).get_duration() == Duration(1, 5)
    assert measure.select_leaves()[1].written_duration == Duration(1, 4)
    assert inspect(measure.select_leaves()[1]).get_duration() == Duration(4, 45)
