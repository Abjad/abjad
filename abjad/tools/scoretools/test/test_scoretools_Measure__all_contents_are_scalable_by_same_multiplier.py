# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_01():

    measure = abjad.Measure((1, 4), "c'4")
    assert measure._all_contents_are_scalable_by_multiplier(abjad.Multiplier(1, 2))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_02():

    measure = abjad.Measure((1, 4), "c'4")
    assert measure._all_contents_are_scalable_by_multiplier(abjad.Multiplier(2, 1))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_03():

    measure = abjad.Measure((1, 4), "c'4")
    assert not measure._all_contents_are_scalable_by_multiplier(
        abjad.Multiplier(2, 3))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_04():

    measure = abjad.Measure((1, 4), "c'4")
    assert measure._all_contents_are_scalable_by_multiplier(abjad.Multiplier(3, 2))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_05():

    measure = abjad.Measure((3, 16), "c'8.")
    assert measure._all_contents_are_scalable_by_multiplier(abjad.Multiplier(2, 3))


def test_scoretools_Measure__all_contents_are_scalable_by_same_multiplier_06():

    measure = abjad.Measure((3, 16), "c'8.")
    assert not measure._all_contents_are_scalable_by_multiplier(
        abjad.Multiplier(3, 2))
