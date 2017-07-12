# -*- coding: utf-8 -*-
import abjad
import copy


def test_scoretools_MultimeasureRest___copy___01():

    multi_measure_rest_1 = abjad.MultimeasureRest((1, 4))
    multi_measure_rest_2 = copy.copy(multi_measure_rest_1)

    assert isinstance(multi_measure_rest_1, abjad.MultimeasureRest)
    assert isinstance(multi_measure_rest_2, abjad.MultimeasureRest)
    assert format(multi_measure_rest_1) == format(multi_measure_rest_2)
    assert multi_measure_rest_1 is not multi_measure_rest_2
