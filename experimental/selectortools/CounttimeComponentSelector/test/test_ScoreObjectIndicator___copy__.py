from abjad.tools import measuretools
from experimental import selectortools
import copy


def test_ScoreObjectIndicator___copy___01():

    indicator_1 = selectortools.CounttimeCounttimeComponentSelector(
        segment='red', context='Voice 1', klass=measuretools.Measure)
    indicator_2 = copy.deepcopy(indicator_1)

    assert isinstance(indicator_1, selectortools.CounttimeCounttimeComponentSelector)
    assert isinstance(indicator_2, selectortools.CounttimeCounttimeComponentSelector)
    assert not indicator_1 is indicator_2
    assert indicator_1 == indicator_2
