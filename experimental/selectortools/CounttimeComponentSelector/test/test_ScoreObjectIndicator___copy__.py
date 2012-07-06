from abjad.tools import measuretools
from experimental import selectortools
import copy


def test_ScoreObjectIndicator___copy___01():

    indicator_1 = selectortools.CounttimeComponentSelector(
        segment='red', context='Voice 1', klass=measuretools.Measure)
    indicator_2 = copy.deepcopy(indicator_1)

    assert isinstance(indicator_1, selectortools.CounttimeComponentSelector)
    assert isinstance(indicator_2, selectortools.CounttimeComponentSelector)
    assert not indicator_1 is indicator_2
    assert indicator_1 == indicator_2
