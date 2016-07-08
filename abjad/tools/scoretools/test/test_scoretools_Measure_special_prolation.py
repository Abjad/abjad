# -*- coding: utf-8 -*-
from abjad import *


# TODO: rename to Measure_implicit_scaling or move there if already exists

def test_scoretools_Measure_special_prolation_01():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    measure = Measure((4, 4), Note("c'4") * 4)

    assert measure[0].written_duration == Duration(1, 4)
    assert inspect_(measure[0]).get_duration() == Duration(1, 4)


def test_scoretools_Measure_special_prolation_02():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    music = [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4"),
        ]
    measure = Measure((4, 4), music)
    leaves = select(measure).by_leaf()

    assert leaves[0].written_duration == Duration(1, 4)
    assert inspect_(leaves[0]).get_duration() == Duration(1, 4)
    assert leaves[1].written_duration == Duration(1, 4)
    assert inspect_(leaves[1]).get_duration() == Duration(1, 6)


def test_scoretools_Measure_special_prolation_03():
    r'''Measures with power-of-two time signature denominator
    contribute trivially to contents prolation.
    '''

    music = [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), [
            scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4"),
        ]
    measure = Measure((4, 4), music)
    leaves = select(measure).by_leaf()

    assert leaves[0].written_duration == Duration(1, 4)
    assert inspect_(leaves[0]).get_duration() == Duration(1, 4)
    assert leaves[1].written_duration == Duration(1, 4)
    assert inspect_(leaves[1]).get_duration() == Duration(1, 9)


def test_scoretools_Measure_special_prolation_04():
    r'''Measures with power-of-two time signature denominators
    and implicit scaling scale the duration of their contents.
    '''

    measure = Measure((4, 5), "c'4 d'4 e'4 f'4")
    measure.implicit_scaling = True

    assert measure[0].written_duration == Duration(1, 4)
    assert inspect_(measure[0]).get_duration() == Duration(1, 5)


def test_scoretools_Measure_special_prolation_05():
    r'''Measures with power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    music = [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
        Note("c'4"),
        ]
    measure = Measure((4, 5), music)
    measure.implicit_scaling = True
    leaves = select(measure).by_leaf()

    assert leaves[0].written_duration == Duration(1, 4)
    assert inspect_(leaves[0]).get_duration() == Duration(1, 5)
    assert leaves[1].written_duration == Duration(1, 4)
    assert inspect_(leaves[1]).get_duration() == Duration(2, 15)


def test_scoretools_Measure_special_prolation_06():
    r'''Measures with power-of-two time signature denominators
    contribute nontrivially to prolation.
    '''

    music = [
        Note("c'4"),
        scoretools.FixedDurationTuplet(Duration(2, 4), [
            scoretools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3),
            Note("c'4")]),
        Note("c'4"),
        ]
    measure = Measure((4, 5), music)
    measure.implicit_scaling = True
    leaves = select(measure).by_leaf()

    assert leaves[0].written_duration == Duration(1, 4)
    assert inspect_(leaves[0]).get_duration() == Duration(1, 5)
    assert leaves[1].written_duration == Duration(1, 4)
    assert inspect_(leaves[1]).get_duration() == Duration(4, 45)
