from abjad.tools import measuretools
from experimental import specificationtools
import copy


def test_ScoreSliceIndicator___copy___01():

    indicator_1 = specificationtools.ScoreSliceIndicator(
        segment='red', context='Voice 1', klass=measuretools.Measure)
    indicator_2 = copy.deepcopy(indicator_1)

    assert isinstance(indicator_1, specificationtools.ScoreSliceIndicator)
    assert isinstance(indicator_2, specificationtools.ScoreSliceIndicator)
    assert not indicator_1 is indicator_2
    assert indicator_1 == indicator_2
