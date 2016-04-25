# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_01():

    measure = Measure((1, 4), "c'4")
    assert measure._all_contents_are_scalable_by_multiplier(Multiplier(1, 2))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_02():

    measure = Measure((1, 4), "c'4")
    assert measure._all_contents_are_scalable_by_multiplier(Multiplier(2, 1))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_03():

    measure = Measure((1, 4), "c'4")
    assert not measure._all_contents_are_scalable_by_multiplier(
        Multiplier(2, 3))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_04():

    measure = Measure((1, 4), "c'4")
    assert measure._all_contents_are_scalable_by_multiplier(Multiplier(3, 2))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_05():

    measure = Measure((3, 16), "c'8.")
    assert measure._all_contents_are_scalable_by_multiplier(Multiplier(2, 3))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_06():

    measure = Measure((3, 16), "c'8.")
    assert not measure._all_contents_are_scalable_by_multiplier(
        Multiplier(3, 2))
