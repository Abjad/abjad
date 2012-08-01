from abjad.tools import measuretools
from experimental import selectortools
import copy


def test_CounttimeComopnentSelector___copy___01():

    indicator_1 = selectortools.SingleContextCounttimeComponentItemSelector('Voice 1', klass=measuretools.Measure)
    indicator_2 = copy.deepcopy(indicator_1)

    assert isinstance(indicator_1, selectortools.SingleContextCounttimeComponentItemSelector)
    assert isinstance(indicator_2, selectortools.SingleContextCounttimeComponentItemSelector)
    assert not indicator_1 is indicator_2
    assert indicator_1 == indicator_2
