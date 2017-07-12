# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Measure_is_misfilled_01():

    measure = abjad.Measure((3, 4), "c' d' e'")
    assert not measure.is_misfilled


def test_scoretools_Measure_is_misfilled_02():

    measure = abjad.Measure((3, 4), "c' d' e' f'")
    assert measure.is_misfilled
