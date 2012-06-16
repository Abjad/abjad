from abjad import *
import copy


def test_MultiMeasureRest___copy___01():

    multi_measure_rest_1 = resttools.MultiMeasureRest((1, 4))
    multi_measure_rest_2 = copy.copy(multi_measure_rest_1)

    assert isinstance(multi_measure_rest_1, resttools.MultiMeasureRest)
    assert isinstance(multi_measure_rest_2, resttools.MultiMeasureRest)
    assert multi_measure_rest_1.lilypond_format == multi_measure_rest_2.lilypond_format
    assert multi_measure_rest_1 is not multi_measure_rest_2
