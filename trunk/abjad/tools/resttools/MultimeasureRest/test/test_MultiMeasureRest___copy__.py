from abjad import *
import copy


def test_MultiMeasureRest___copy___01():

    multi_measure_rest_1 = resttools.MultimeasureRest((1, 4))
    multi_measure_rest_2 = copy.copy(multi_measure_rest_1)

    assert isinstance(multi_measure_rest_1, resttools.MultimeasureRest)
    assert isinstance(multi_measure_rest_2, resttools.MultimeasureRest)
    assert multi_measure_rest_1.lilypond_format == multi_measure_rest_2.lilypond_format
    assert multi_measure_rest_1 is not multi_measure_rest_2
